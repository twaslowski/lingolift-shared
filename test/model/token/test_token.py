import pytest

from shared.model.token.feature import Case, Gender, NounFeatureSet, Number
from shared.model.token.token import Token
from shared.model.token.upos import UPOS


@pytest.fixture
def feature_set():
    return NounFeatureSet(case=Case.NOM, number=Number.SING, gender=Gender.FEM)


@pytest.fixture
def minimal_token():
    return Token(text="ancestor_text", lemma="ancestor_text", upos=UPOS.NOUN)


@pytest.fixture
def complete_token(feature_set, minimal_token):
    return Token(
        text="text",
        lemma="base-text",
        upos=UPOS.ADJ,
        feature_set=feature_set,
        ancestor=minimal_token,
    )


def test_to_string_for_all_fields_set(complete_token):
    assert (
        complete_token.__str__()
        == "(from: base-text);  refers to: ancestor_text; Adjective; Nominative Singular Feminine"
    )


def test_to_string_for_some_fields(minimal_token):
    assert minimal_token.__str__() == "Noun"


def test_to_string_for_some_fields_with_lemma(minimal_token):
    minimal_token.lemma = "lemma"
    assert minimal_token.__str__() == "(from: lemma); Noun"
