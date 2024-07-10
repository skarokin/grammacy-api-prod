# checks if sentence ends with punctuation
import string

def check_punctuation(input_text, _):
    if input_text.text[-1] not in string.punctuation:
        return 'Sentence must end with punctuation', input_text[-1].i + 1, '.'
    return None, None, None