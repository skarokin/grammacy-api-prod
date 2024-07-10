# 1. their/there (cant do they're because spacy splits it into they and 're)
# 2. affect/effect
# 3. to/too/two
# 4. then/than
# TODO: Higher augmentation probability for their/there, then/than, and MAYBE to/too/two. Also find more homophones!
def check_homophones(input_text, _):
    for tok in input_text:
        # affect used as a noun
        if tok.text.lower().startswith("affect") and tok.pos_ == "NOUN":
            return "Use 'effect' instead of 'affect' as a noun", tok.i, "effect" + tok.text[6:]
        # effect used as a verb
        if tok.text.lower().startswith("effect") and tok.pos_ == "VERB":
            return "Use 'affect' instead of 'effect' as a verb", tok.i, "affect" + tok.text[6:]
        # then used as a preposition
        if tok.text.lower() == "then" and tok.dep_ == "case":
            return "Use 'than' instead of 'then' as a preposition", tok.i, "than"
        # too/two used as a preposition
        if tok.text.lower() in ("too", "two") and tok.dep_ == "case":
            return f"Use 'to' instead of '{tok.text}' as a preposition", tok.i, "to"
        # to/too used as a numeric modifier
        if tok.text.lower() in ("to", "too") and tok.dep_ == "nummod":
            return f"Use 'two' instead of '{tok.text}' as a numeric modifier", tok.i, "two"
        # two/to used as an adverb
        if tok.text.lower() in ("two", "to") and tok.dep_ == "advmod":
            return f"Use 'too' instead of '{tok.text}' as an adverb", tok.i, "too"
        # there used as a possessive pronoun
        if tok.text.lower() == "there" and tok.dep_ == "nmod:poss":
            return "Use 'their' instead of 'there' as a possessive pronoun", tok.i, "their"
        # their used as expletive
        if tok.text.lower() == "their" and tok.dep_ == "expl":
            return "Use 'there' instead of 'their' as an expletive", tok.i, "there"
    return None, None, None