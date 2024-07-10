import json

def predict_errors(sentence: str, egm, esm):
    grammar_result = json.loads(egm.enforce(sentence))
    spelling_result = json.loads(esm.enforce(sentence))
    
    return {
        'grammar_errors': grammar_result,
        'spelling_errors': spelling_result,
    }