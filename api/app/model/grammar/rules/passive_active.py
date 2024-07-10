# flags passive voice as a styling error, does not return a suggestion (since not technically an error and also hard to suggest a fix)
# simply analyzes if nsubjpass, auxpass, or csubjpass are present in the sentence
def check_passive_active(input_text, _):
    for tok in input_text:
        if tok.dep_ in ('nsubj:pass', 'aux:pass', 'csubj:pass'):
            return 'Sentence is possibly passive voice', tok.i, ''
    return None, None, None