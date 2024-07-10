import json
import string

class EnglishSpellingModel:
    def __init__(self, sym_spell):
        self.sym_spell = sym_spell

    def enforce(self, input_text):
        # symspell ignores punctuation, so to simplify comparison we remove punctuation from input text
        input_text = self.remove_punctuation(input_text)

        suggestions = self.sym_spell.lookup_compound(
            input_text, max_edit_distance=2, transfer_casing=True, ignore_non_words=True, ignore_term_with_digits=True, split_by_space=True
        )

        suggestions_str = [word for suggestion in suggestions for word in str(suggestion.term).split()]

        errors = []

        for original, suggestion in zip(input_text.split(), suggestions_str):
            if original != suggestion:
                errors.append({
                    original: suggestion
                })

        return json.dumps({
            "errors": errors
        })
    
    def remove_punctuation(self, input_text):
        return input_text.translate(str.maketrans('', '', string.punctuation))