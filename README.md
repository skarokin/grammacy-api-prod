# grammacy-api-prod
Our production-ready API to serve real-time English grammar and spell checking.
- Grammar checker built with [grammacy](https://github.com/skarokin/grammacy) 
- Integrated [symspellpy](https://github.com/mammothb/symspellpy) for spell checking

This API is CPU-optimized and uses fast, lightweight models while retaining a high level of accuracy.

### architecture
- Grammar and spell checkers built as a Flask endpoint, running on Gunicorn
- NGINX reverse proxy for SSL termination and whitelisting
- Certbot for SSL certification with a cron job for auto-renewal (Certbot directory is gitignored for security)
- Containerized with Docker Compose
- Deployed on AWS EC2

### grammar rules
The following grammar rules are enforced based on dependency parse trees, POS tags, and morphological features. To suggest another rule or a modification of an existing one, you can visit my [website](https://www.skarokin.com) for contact information.
- Verbs after modals must be in base form
- Adjective/adverb confusion
- Adverbs cannot be used as the complement of a copula
- Verbs are prepositions must be in base form
- Passive voice detection
- Subject-verb agreement
- Complete sentence check
- Copula/auxiliary verbs must agree with their subjects
- Sentences must end with a punctuation
- Sentences must begin with a capital word
- Gerunds not at the beginning of a sentence must be part of a verb phrase
- 'A' vs 'An'
- 'I' must always be capitalized
- Pronoun-antecedent agreement
- Subjective pronouns cannot be used in the accusative case
- Objective pronouns cannot be used in the nominal case
- Some common homophones
- Prepositions must be followed by a noun or another preposition
- Prepositions cannot be preceded by a determiner or proper noun
- Determiners must be followed by a noun or adjective