obj_to_subj = {
    'me': 'i',
    'him': 'he',
    'her': 'she',
    'us': 'we',
    'them': 'they',
}

subj_to_obj = {v: k for k, v in obj_to_subj.items()}

def check_subjective_objective(input_text, _):
    for tok in input_text:
        # ensure if child of iobj is a pronoun, that it is objective/accusative
        if tok.dep_ in ('iobj', 'obj') and tok.text.lower() in subj_to_obj:
            corrected_pronoun = subj_to_obj[tok.text.lower()] if tok.text.lower() in subj_to_obj else None
            return 'A subjective pronoun cannot be used in the accusative case', tok.i, corrected_pronoun

        # ensure if child of nsubj is a pronoun, that it is subjective/nominal
        elif tok.dep_ == 'nsubj' and tok.text.lower() in obj_to_subj:
            corrected_pronoun = obj_to_subj[tok.text.lower()] if tok.text.lower() in obj_to_subj else None
            if corrected_pronoun == 'i':
                corrected_pronoun = 'I'
            return 'An objective pronoun cannot be used in the nominal case', tok.i, corrected_pronoun
    return None, None, None