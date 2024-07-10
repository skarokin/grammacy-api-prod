# check if word preceeding or following the preposition is viable
def check_prepositions(input_text, _):
    for tok in input_text:
        if tok.tag_ == 'IN' and tok.dep_ == 'case':
            if tok.i > 0 and tok.nbor(-1).tag_ in ['PRP', 'DT']:
                return 'A preposition cannot be preceded by a proper noun or determiner', tok.i, ''
            if tok.i < len(input_text) and tok.nbor().pos_ not in ['NOUN', 'PRON', 'DET', 'ADP']:
                return 'A preposition must be followed by a noun or pronoun', tok.i, ''
    return None, None, None