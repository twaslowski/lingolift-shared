import pytest
import spacy

from shared.model.token.feature import (
    Case,
    Gender,
    NounFeatureSet,
    Number,
    Person,
    Tense,
    VerbFeatureSet,
)
from shared.model.token.mapper import from_spacy_doc, from_spacy_token
from shared.model.token.token import UPOS


@pytest.fixture
def nlp():
    return spacy.load("de_core_news_sm")


def test_upos_parsing(nlp):
    doc = list(nlp("Der Tisch hat vier eckige Beine."))

    # first token is "Der"
    token = doc[0]
    assert token.pos_ == "DET"
    result = from_spacy_token(token)
    assert result.upos == UPOS.DET

    # second token is "Tisch"
    token = doc[1]
    assert token.pos_ == "NOUN"
    result = from_spacy_token(token)
    assert result.upos == UPOS.NOUN

    # third token is "hat"
    token = doc[2]
    assert token.pos_ == "VERB"
    result = from_spacy_token(token)
    assert result.upos == UPOS.VERB

    # fourth token is "vier"
    token = doc[3]
    assert token.pos_ == "NUM"
    result = from_spacy_token(token)
    assert result.upos == UPOS.NUM

    # fifth token is "eckige"
    token = doc[4]
    assert token.pos_ == "ADJ"
    result = from_spacy_token(token)
    assert result.upos == UPOS.ADJ


def test_feature_parsing(nlp):
    doc = list(nlp("Der Tisch hat vier eckige Beine."))

    # first token is "Der"
    token = doc[0]
    result = from_spacy_token(token)
    assert type(result.feature_set) is NounFeatureSet
    assert result.feature_set.case == Case.NOM
    assert result.feature_set.number == Number.SING
    assert result.feature_set.gender == Gender.MASC

    # second token is "Tisch"
    token = doc[1]
    result = from_spacy_token(token)
    assert type(result.feature_set) is NounFeatureSet
    assert result.feature_set.case == Case.NOM
    assert result.feature_set.number == Number.SING
    assert result.feature_set.gender == Gender.MASC

    # third token is "hat"
    token = doc[2]
    result = from_spacy_token(token)
    assert type(result.feature_set) is VerbFeatureSet
    assert result.feature_set.tense is Tense.PRES
    assert result.feature_set.number is Number.SING
    assert result.feature_set.person is Person.THIRD


def test_feature_parsing_plural(nlp):
    tokens = from_spacy_doc(nlp("Die Tische haben vier eckige Beine"))
    assert tokens[0].feature_set.number == Number.PLUR
    assert tokens[0].feature_set.case == Case.NOM
    assert tokens[0].feature_set.gender == Gender.MASC

    assert tokens[1].feature_set.number == Number.PLUR
    assert tokens[1].feature_set.case == Case.NOM
    assert tokens[1].feature_set.gender == Gender.MASC


def test_ancestor_mapping(nlp):
    doc = nlp("Der Tisch hat vier eckige Beine.")

    tokens = from_spacy_doc(doc)
    assert tokens[0].ancestor == tokens[1]  # "Der" -> "Tisch"
    assert tokens[4].ancestor == tokens[5]  # "eckige" -> "Beine"
