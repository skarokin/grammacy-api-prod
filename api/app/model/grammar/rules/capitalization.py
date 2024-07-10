# checks if first word of sentence is capitalized
def check_capitalization(input_text, _):
    if input_text[0].text.islower():
        return 'First word of sentence must be capitalized', 0, input_text[0].text.capitalize()

    return None, None, None