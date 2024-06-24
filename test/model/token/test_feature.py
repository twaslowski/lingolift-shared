from shared.model.token.mapper import feature_set_from_dict
from shared.model.token.upos import UPOS


def test_feature_stringification_noun():
    features = {"Case": "Acc", "Number": "Sing", "Gender": "Masc"}
    upos = UPOS.NOUN
    feature_set = feature_set_from_dict(features, upos)
    assert str(feature_set) == "Accusative Singular Masculine"


def test_feature_stringification_verb():
    features = {"Tense": "Past", "Number": "Sing", "Person": "1"}
    upos = UPOS.VERB
    feature_set = feature_set_from_dict(features, upos)
    assert str(feature_set) == "First person Singular Past tense"
