# a gerund cannot be used on its own; it must be preceeeded by a preposition
def check_gerund(input_text, _):
    for tok in input_text:
        if tok.tag_ == 'VBG':
            if tok.i-1 >= 0 and input_text[tok.i-1].pos_ not in ['ADP', 'AUX', 'VERB', 'SCONJ']:
                return 'Gerunds not at the beginning of a sentence must be part of a verb phrase', tok.i-1, ''
    return None, None, None