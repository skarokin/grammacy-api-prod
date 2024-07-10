def check_i(input_text, _):
    for tok in input_text:
        if tok.text == 'i':
            return 'The pronoun "I" must be capitalized', tok.i, 'I'
    return None, None, None