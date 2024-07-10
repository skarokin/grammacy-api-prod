from pathlib import Path
import json

from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

import spacy
import lemminflect
from symspellpy import SymSpell
from model.model import predict_errors

from model.grammar.utils.get_forms import GetForms
from model.grammar.en_grammar_model import EnglishGrammarModel
from model.spelling.en_spelling_model import EnglishSpellingModel

from model.grammar.rules.passive_active import check_passive_active
from model.grammar.rules.sva import check_sva
from model.grammar.rules.complete_sentence import check_complete_sentence
from model.grammar.rules.copula_aux import check_copula_aux
from model.grammar.rules.punctuation import check_punctuation
from model.grammar.rules.capitalization import check_capitalization
from model.grammar.rules.gerund import check_gerund
from model.grammar.rules.a_an import check_a_an
from model.grammar.rules.i import check_i
from model.grammar.rules.pronoun_agreement import check_pronoun_agreement
from model.grammar.rules.subjective_objective import check_subjective_objective
from model.grammar.rules.homophones import check_homophones
from model.grammar.rules.prepositions import check_prepositions
from model.grammar.rules.determiners import check_determiners

# just for ease of debugging
BASE_DIR = Path(__file__).resolve(strict=True).parent

# -----------------------------------------------------------
#                LOAD GRAMMAR CHECKING MODEL
# -----------------------------------------------------------
# models are named english-vx.y where x = dataset version and y = training version
# - v0: augmented OntoNotes 5.0
# - v1: augmented OntoNotes 5.0
# - v2: augmented OntoNotes 5.0 + unaugmented GUM 
# - v3: augmented OntoNotes 5.0 + unaugmented GUM (more augmentations than v2)
# - v4: augmented GUM
# the model used in production is v4.11 (see model/grammar/english-v4.11-prod for training config and metrics)
# GUM was used in the final model because it has more modern text and has morph feat data
MODEL_VER = 'english-v4.11-prod'

nlp = spacy.load(f'{BASE_DIR}/model/grammar/{MODEL_VER}')

with open(f"{BASE_DIR}/model/grammar/utils/adj_to_adv.txt", 'r') as f:
    ADJECTIVE_TO_ADVERB = json.load(f)

with open(f"{BASE_DIR}/model/grammar/utils/adv_to_adj.txt", 'r') as f:
    ADVERB_TO_ADJECTIVE = json.load(f)

rules = [
    ('aux', ['MD'], ['VBG', 'VBD', 'VBZ'], 'VB', False, 'Verbs after modals should be in base form'),
    ('advmod', ['JJ'], ['VB', 'VBD', 'VBZ', 'VBN', 'VBP', 'NN', 'NNP'], 'RB', True, 'Adjective/adverb confusion: use an adverb instead'),
    ('cop', ['VB', 'VBD', 'VBZ', 'VBN', 'VBP'], ['RB'], 'JJ', False, 'An adverb cannot be used as the complement of a copula verb, use an adjective instead'),
    ('case', ['IN'], ['VB', 'VBD', 'VBZ', 'VBN', 'VBP'], 'VBG', False, 'A verb after a preposition should be in gerund form'),
    check_passive_active,
    check_sva,
    check_complete_sentence,
    check_copula_aux,
    check_punctuation,
    check_capitalization,
    check_gerund,
    check_a_an,
    check_i,
    check_pronoun_agreement,
    check_subjective_objective,
    check_homophones,
    check_prepositions,
    check_determiners
]

gf = GetForms(nlp, lemminflect, ADJECTIVE_TO_ADVERB, ADVERB_TO_ADJECTIVE)
egm = EnglishGrammarModel(nlp, gf, rules)

# -----------------------------------------------------------
#                LOAD SPELL CHECKING MODEL
# -----------------------------------------------------------
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = f'{BASE_DIR}/model/spelling/utils/frequency_dictionary_en_82_765.txt'
bigram_path = f'{BASE_DIR}/model/spelling/utils/frequency_bigramdictionary_en_243_342.txt'

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

esm = EnglishSpellingModel(sym_spell)

# -----------------------------------------------------------
#                FLASK APP
# -----------------------------------------------------------
app = Flask(__name__)

# necessary for running behind Nginx reverse proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

def clean_text(text):
    return text.rstrip().lstrip()
 
@app.route("/", methods=['GET'])
def index():
    return jsonify({'status': 'OK', 'model': MODEL_VER})

@app.route("/predict", methods=['POST'])
def predict():
    payload = request.form.get('input')

    # type checking
    if type(payload) != str:
        return {"error": "Input text must be a string."}
    if payload is None:
        return {"error": "Input text is null."}
    
    payload = clean_text(payload)
    
    # length checking (model is extremely efficient, but data transfer out of EC2 is expensive lol)
    if len(payload) == 0:
        return {"error": "Input text is empty."}
    if len(payload) > 256:
        return {"error": "Input text is too long."}
    
    result = predict_errors(payload, egm, esm)
    return {"result": result}

# for local testing. in production, Gunicorn is used to run the server (see Dockerfile)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)