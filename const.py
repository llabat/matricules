import string

# Search parameters
letters = list(string.ascii_lowercase) # all lowercase letters from the latin alphabet
bigrams = [l1+l2 for l1 in letters for l2 in letters]
classes = [str(i) for i in range(1887,1922)]

SEARCH_COMBINATIONS = [(bigram, clas) for bigram in bigrams for clas in classes]

COMPLEMENT = "https://archives.paris.fr/"

PARIS_WEBSITE = 'https://archives.paris.fr/s/17/-ats-signaletiques-et-des-services-militaires/?'

# Scroll-down menu options (3rd search parameter : bureau de recrutement)
BUREAU1 = 'MWVyIGJ1cmVhdQ=='
BUREAU2 = 'MmUgYnVyZWF1'
BUREAU3 = 'M2UgYnVyZWF1'
BUREAU4 = 'NGUgYnVyZWF1'
BUREAU6 = 'NmUgYnVyZWF1'
RECRUTEXT = 'UmVjcnV0ZW1lbnQgZXh06XJpZXVy'

BUREAUX = [BUREAU1, BUREAU2, BUREAU3, BUREAU4, BUREAU6, RECRUTEXT]


