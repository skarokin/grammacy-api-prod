# TO DO: Ensure that we consider tense of verb AND noun
map = {
    'VBD': 'past',
    'VBN': 'past',
    'VBG': 'present',
    'VBP': 'present',
    'VBZ': 'present',
    'VB': 'base',
}

def check_future_tense(head, child):
    if head.tag_ in ('MD', 'VB') and child.tag_ in ('VB', 'VBG'):
        return True
    return False

def check_verb_tense(input_text, get_forms):
    first_word_tense = None
    first_word_tag = None
    for tok in input_text:
        if tok.pos_ in ['VERB', 'NOUN']:
            if first_word_tense is None:
                first_word_tense = 'future' if check_future_tense(tok.head, tok) else map[tok.tag_]
                first_word_tag = tok.tag_
            else:
                curr_word_tense = 'future' if check_future_tense(tok.head, tok) else map[tok.tag_]
                if first_word_tense != curr_word_tense:
                    return 'Possibly inconsistent verb tense', tok.i, get_forms.get_forms(tok.text, first_word_tag)
                
    return None, None, None