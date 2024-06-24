from enum import Enum


class UPOS(Enum):
    """
    Replaces the previous PartOfSpeech class.
    This is a structured way of representing the Universal POS tags, which are contained as strings in spaCy tokens.
    Reference: https://universaldependencies.org/u/pos/
    """

    # Open class words
    ADJ = "adjective"
    ADV = "adverb"
    INTJ = "interjection"
    NOUN = "noun"
    PROPN = "proper noun"
    VERB = "verb"

    # Closed class words
    ADP = "adposition"
    AUX = "auxiliary verb"
    CCONJ = "coordinating conjunction"
    DET = "determiner"
    NUM = "numeral"
    PART = "particle"
    PRON = "pronoun"
    SCONJ = "subordinating conjunction"

    # Other
    PUNCT = "punctuation"
    SYM = "symbol"
    X = "other"

    def is_noun_like(self):
        """
        Determines if a token is likely to have features common to nouns (e.g. case, gender, number).
        """
        return self in {UPOS.NOUN, UPOS.PROPN, UPOS.PRON, UPOS.DET, UPOS.ADJ}

    def is_verb_like(self):
        """
        Determines if a token is likely to have features common to verbs (e.g. tense, person, number).
        """
        return self in {UPOS.VERB, UPOS.AUX}
