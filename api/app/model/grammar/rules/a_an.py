# a vs an
def check_a_an(input_text, _):
    for tok in input_text:
        if tok.tag_ == 'DT':
            if tok.text.lower() == 'a' and tok.nbor().text[0].lower() in 'aeiou':
                return 'Use an instead of a before a word that starts with a vowel sound', tok.i, 'an'
            elif tok.text.lower() == 'an' and tok.nbor().text[0].lower() not in 'aeiou':
                return 'Use a instead of an before a word that starts with a consonant sound', tok.i, 'a'
    return None, None, None