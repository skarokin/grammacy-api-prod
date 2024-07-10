# special case: 'to be' copula
# since PTB interprates was/were as VBD, and am/are as VBP, we need a special check for 'to be' specifically
# - use the plurality and tense of the subject to determine if the copula is correct
# - we can use the tense of the copula to return past/present forms of the singular/plural and 1st/2nd/3rd person forms
# we are going through all of this trouble because 'to be' is like 90% of copula errors and the 6 PTB tags don't cut it
# i have an idea for a future release of grammaCy that leverages an in-house inflection engine to make this more accurate, and it
# doesn't rely on PTB tags and only CoNLL-U part of speeches with morphological features
def check_copula_aux(input_text, get_forms):
    for tok in input_text:
        if tok.dep_ in ('cop', 'aux'):
            subj = find_subject(tok.head)

            if subj is None:
                continue

            # a hard-coded check for 'to be' because it's such a common error that we want to be as accurate as possible
            if tok._.lemma() == 'be':
                return to_be(tok, subj)
            elif subj.morph.get('Number') and subj.morph.get('Number')[0] == 'Sing' and tok.morph.get('Number') and tok.morph.get('Number')[0]  == 'Plur': 
                return 'Copula error: Copula is plural and subject is singular', tok.i, [
                    get_forms.get_forms(tok.text, 'VBZ'), get_forms.get_forms(tok.text, 'VBD')]
            
            elif subj.morph.get('Number') and subj.morph.get('Number')[0] == 'Plur' and tok.morph.get('Number') and tok.morph.get('Number')[0] == 'Sing':
                return 'Copula error: Copula is singular and subject is plural', tok.i, [
                    get_forms.get_forms(tok.text, 'VBP'), get_forms.get_forms(tok.text, 'VBD')]

    return None, None, None
            
def find_subject(tok):
    for child in tok.children:
        if child.dep_ in ['nsubj', 'nsubjpass']:
            return child
    return None

def to_be(tok, subj):
    subj_plurality = subj.morph.get('Number')[0]
    # if no person, use verb's person. if verb has no person, assume 3rd person. if verb has no tense, assume present
    subj_person = int(subj.morph.get('Person')[0] if subj.morph.get('Person') else tok.morph.get('Person')[0] if tok.morph.get('Person') else 3)
    intended_tense = tok.morph.get('Tense')[0] if tok.morph.get('Tense') else 'Pres'     

    # 1st person singular present, should be 'am'
    if subj_plurality == 'Sing' and subj_person == 1 and intended_tense == 'Pres' and tok.text not in ('am', "'m"):
        return 'Copula/aux error: Use am for 1st person singular present', tok.i, 'am'
    # 1st person singular past OR 3rd person singular past, should be 'was'
    elif subj_plurality == 'Sing' and (subj_person == 1 or subj_person == 3) and intended_tense == 'Past' and tok.text != 'was':
        return 'Copula/aux error: Use was for 1st/3rd person singular past', tok.i, 'was'
    # 2nd person singular present OR 1st/2nd/3rd person plural present, should be 'are'
    elif (subj_plurality == 'Sing' and subj_person == 2) or (subj_plurality == 'Plur') and intended_tense == 'Pres' and tok.text not in ("are", "'re"):
        return 'Copula/aux error: Use are for 2nd person singular present', tok.i, 'are'
    # 2nd person singular past OR 1st/2nd/3rd person plural past, should be 'were'
    elif (subj_plurality == 'Sing' and subj_person == 2) or (subj_plurality == 'Plur') and intended_tense == 'Past' and tok.text != 'were':
        return 'Copula/aux error: Use were for 2nd person singular past', tok.i, 'were'
    # 3rd person singular present, should be 'is'
    elif subj_plurality == 'Sing' and subj_person == 3 and intended_tense == 'Pres' and tok.text != 'is':
        return 'Copula/aux error: Use is for 3rd person singular present', tok.i, 'is'
    return None, None, None