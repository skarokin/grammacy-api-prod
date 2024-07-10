import json
# NOTE: our API is containerized and kept alive with the spaCy pipeline and get_forms function already loaded in memory
#       this ensures low latency by avoiding the overhead of loading the pipeline and get_forms function for each request
#       thus the constructor requires the pipeline and get_forms function to be passed in as arguments
# this English model is fine tuned for these specific rules but can be easily extended to include more rules
# - subject-verb agreement
# - adjective/adverb confusion
# - correct verb form (all kinds of cases, like verbs after {prepositions, auxiliaries, etc})
# - correct auxiliary verb form (to be, to have, to do, etc)
# - complete sentence check
# - correct comparative usage
# - consistent verb tense
# - subject-verb-object order check
class EnglishGrammarModel:
    def __init__(self, nlp, get_forms, rules):
        '''
        nlp: a spaCy pipeline
        get_forms: a function that takes (word, lemma, tag) and returns the desired tag form of that word
        rules: a list of either tuples or functions that enforce rules on the input text
              [(dep_rel, child_tag_list, head_tag_list, correct_tag_list, enforce_child_or_head, error_message), ...]
              a function as a rule must take a Doc object and get_forms as input and return (error_message, corrected_word_index, corrected_word)
        '''
        self.nlp = nlp
        self.get_forms = get_forms    
        self.rules = rules
    
    def enforce(self, input_text):
        input_text = self.nlp(input_text)

        errors = []
        for rule in self.rules:
            if callable(rule):
                # call rule(self.input_text, self.get_forms) where input_text is a Doc object
                # rule should return (error_message, corrected_word_index, corrected_word)
                error_message, corrected_word_index, corrected_word = rule(input_text, self.get_forms)
                if error_message and corrected_word is not None:
                    errors.append((error_message, corrected_word_index, corrected_word))
            else:
                dep_rel, child_tag_list, head_tag_list, correct_tag, child, error_message = rule
                for token in input_text:
                    if token.dep_ == dep_rel and token.head.tag_ in head_tag_list and token.tag_ in child_tag_list:
                        # if child is False, then head should be in the whitelist of correct tags
                        if not child and token.head.tag_ != correct_tag:
                            suggestion = self.get_forms.get_forms(token.head.text, correct_tag)
                            if suggestion is not None:
                                errors.append((error_message, token.head.i, suggestion))
                        # else, child should be in the whitelist of correct tags
                        elif token.tag_ != correct_tag:
                            suggestion = self.get_forms.get_forms(token.text, correct_tag)
                            if suggestion is not None:
                                errors.append((error_message, token.i, suggestion))
        return self.format_errors(errors)
    
    def format_errors(self, errors):
        return json.dumps({
            "errors": [{"error": error_message, "corrected_word_index": corrected_word_index, "suggestion": suggestion} 
                       for error_message, corrected_word_index, suggestion in errors]
        })