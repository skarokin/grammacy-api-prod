def check_determiners(input_text, _):
    for tok in input_text:
        if tok.tag_ == 'DT' and ((tok.i < len(input_text) and tok.nbor().pos_ not in ['NOUN', 'ADJ']) or (tok.i == len(input_text)-1)):
            return 'Determiners must be followed by a noun or adjective', tok.i, ''
    return None, None, None