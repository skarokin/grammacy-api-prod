import json
import os

# get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(script_dir, '../utils/genders.json')

with open(file_path, 'r') as f:
    gender_map = json.load(f)

# word: [masc, fem, neut]
pronouns_map = {
    'he': ['he', 'she', 'they'],
    'him': ['his', 'her', 'them'],
    'his': ['his', 'her', 'their'],
    'himself': ['himself', 'herself', 'themselves'],
    'she': ['he', 'she', 'they'],
    'her': ['his', 'her', 'them'],
    'hers': ['his', 'her', 'their'],
    'herself': ['himself', 'herself', 'themselves'],
    'they': ['he', 'she', 'they'],
    'them': ['his', 'her', 'them'],
    'their': ['his', 'her', 'their'],
    'themselves': ['himself', 'herself', 'themselves'],
}

def check_pronoun_agreement(input_text, get_forms):
    antecedent_number = None
    antecedent_gender = None

    for tok in input_text:
        if not antecedent_number and not antecedent_gender and tok.dep_ in ['nsubj', 'nsubj:pass']:
            antecedent_number = tok.morph.get('Number')[0] if tok.morph.get('Number') else 'Sing' # assume singular if not found
            antecedent_gender = gender_map[tok.text.lower()] if tok.text.lower() in gender_map else 'Neut' # assume neutral if not found

        elif tok.tag_ in ['PRP', 'PRP$']:
            if tok.morph.get('Gender'):
                if antecedent_gender == 'Masc' and tok.morph.get('Gender')[0] != 'Masc':
                    return 'Pronoun should be masculine to match antecedent', tok.i, pronouns_map[tok.text.lower()][0] if tok.text.lower() in pronouns_map else None
                elif antecedent_gender == 'Fem' and tok.morph.get('Gender')[0] != 'Fem':
                    return 'Pronoun should be feminine to match antecedent', tok.i, pronouns_map[tok.text.lower()][1] if tok.text.lower() in pronouns_map else None
            # if pronoun has no gender, it is neutral, so check if antecedent is also neutral
            else:
                if antecedent_gender == 'Masc':
                    return 'Pronoun should be masculine to match antecedent', tok.i, pronouns_map[tok.text.lower()][0] if tok.text.lower() in pronouns_map else None
                elif antecedent_gender == 'Fem':
                    return 'Pronoun should be feminine to match antecedent', tok.i, pronouns_map[tok.text.lower()][1] if tok.text.lower() in pronouns_map else None
            
            if tok.morph.get('Number') and antecedent_number == 'Plur' and tok.morph.get('Number')[0] != 'Plur':
                return 'Pronoun should be plural to match antecedent', tok.i, get_forms.get_forms(tok.text.lower(), 'NNS') 
            elif tok.morph.get('Number') and antecedent_number == 'Sing' and tok.morph.get('Number')[0] != 'Sing':
                return 'Pronoun should be singular to match antecedent', tok.i, get_forms.get_forms(tok.text.lower(), 'NN')

    return None, None, None

    