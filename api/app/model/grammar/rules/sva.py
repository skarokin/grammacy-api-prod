# check for subject-verb agreement
# - uses morph feats to determine intended tense
# - uses morph feats to determine if person of subject matches person of verb (additional layer to reduce false positives)
map = {
    (1, 'Sing', 'Pres') : 'VBP',
    (2, 'Sing', 'Pres') : 'VBP',
    (3, 'Sing', 'Pres') : 'VBZ',
    (1, 'Plur', 'Pres') : 'VBP',
    (2, 'Plur', 'Pres') : 'VBP',
    (3, 'Plur', 'Pres') : 'VBP',
    (1, 'Sing', 'Past') : 'VBD',
    (2, 'Sing', 'Past') : 'VBD',
    (3, 'Sing', 'Past') : 'VBD',
    (1, 'Plur', 'Past') : 'VBD',
    (2, 'Plur', 'Past') : 'VBD',
    (3, 'Plur', 'Past') : 'VBD'
}

def check_sva(input_text, get_forms):
    for tok in input_text:
        # sometimes head is non-verbal. Also, ignore gerunds and participles for this check (its a different rule)
        if tok.dep_ == 'nsubj' and tok.head.pos_ == 'VERB' and tok.head.tag_ in ['VB', 'VBZ', 'VBP', 'VBD']:
            intended_tense = tok.head.morph.get('Tense')[0] if tok.head.morph.get('Tense') else 'Pres' if tok.head.tag_ in ['VB', 'VBZ', 'VBP'] else 'Past'
            subj_person = int(tok.morph.get('Person')[0]) if tok.morph.get('Person') else 3 
            subj_plurality = 'Sing' if tok.morph.get('Number') and tok.morph.get('Number')[0] == 'Sing' else 'Plur' 

            # given the subject's person and plurality, and intended tense of the verb, get the correct verb form
            # TODO: build a custom inflection model to generate verb forms based on tense, person, plurality
            #       for now, use a simple map with the 6 PTB tags
            correct_verb_form = map[(subj_person, subj_plurality, intended_tense)]

            if tok.head.tag_ != correct_verb_form:
                return f'SVA error: Incorrect verb form for {subj_person} person {subj_plurality.lower()} {intended_tense.lower()}', tok.i, get_forms.get_forms(tok.head.text, correct_verb_form)

    return None, None, None