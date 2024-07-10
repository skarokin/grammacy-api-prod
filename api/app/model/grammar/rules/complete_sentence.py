def check_complete_sentence(input_text, _):
    has_verb = False
    has_noun = False

    for tok in input_text: 
        if tok.pos_ == 'VERB' or tok.dep_ == 'cop': 
            has_verb = True 
        elif tok.pos_ in ['NOUN', 'PROPN', 'PRON']:
            has_noun = True 
    
    if has_noun and has_verb: 
        return None,None,None
    elif has_noun: 
        return 'Sentence is missing a verb', '', ''
    elif has_verb:
        return 'Sentence is missing a noun', '', ''
    else: 
        return 'Sentence is missing a noun and a verb', '', '' 


