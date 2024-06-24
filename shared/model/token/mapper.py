from enum import Enum, EnumMeta
from typing import TypeVar

from spacy.tokens import Doc
from spacy.tokens.token import Token as SpacyToken

from shared.model.token.feature import (
    Case,
    FeatureSet,
    Gender,
    NounFeatureSet,
    Number,
    Person,
    Tense,
    VerbFeatureSet,
)
from shared.model.token.token import Token as LLToken
from shared.model.token.upos import UPOS

# Relevant to the parse() function
T = TypeVar("T", bound=Enum)


def from_spacy_doc(doc: Doc) -> list[LLToken]:
    """
    Converts a list of spaCy tokens to a list of more structured Token objects.
    """
    spacy_tokens = list(doc)
    ll_tokens = [from_spacy_token(token) for token in spacy_tokens]
    return enrich_ll_tokens_with_ancestors(ll_tokens, spacy_tokens)


def enrich_ll_tokens_with_ancestors(
    ll_tokens: list[LLToken], spacy_tokens: list[SpacyToken]
) -> list[LLToken]:
    """
    Enriches a list of lingolift tokens with information about their respective ancestors in the dependency tree.
    Currently only works at depth 1, i.e. only a token's immediate parent is considered.
    Assumes that the order of the tokens in each list is identical.
    """
    # Create a dictionary for faster lookup of tokens by their text content
    ll_tokens_by_text = {token.text: token for token in ll_tokens}
    for ll_token, spacy_token in zip(ll_tokens, spacy_tokens):
        # For the current lingolift token, find the corresponding spaCy token's ancestor in its dependency tree
        ancestor = next(spacy_token.ancestors, None)
        # If one is found, find the corresponding lingolift token and assign it as the ancestor
        # This could perhaps be made easier with the assumption that the order of the tokens is identical
        if ancestor is not None:
            ancestor_ll_token = ll_tokens_by_text.get(ancestor.text)
            ll_token.ancestor = ancestor_ll_token
    return ll_tokens


def from_spacy_token(token: SpacyToken) -> LLToken:
    """
    Converts a spaCy token to a more structured Token object.
    Because this function refers to a singular token without context,
    it does not take into account dependencies between words.
    For that, use from_spacy_doc().
    """
    return LLToken(
        text=token.text,
        lemma=token.lemma_,
        upos=map_upos(token),
        feature_set=map_feature_set(token),
    )


def map_upos(token: SpacyToken) -> UPOS:
    """
    Maps a UPOS string from spaCy to the UPOS enum.
    """
    return parse(token.pos_, UPOS)


def map_feature_set(token: SpacyToken) -> FeatureSet | None:
    """
    Extracts a FeatureSet from a spaCy token.
    """
    upos = map_upos(token)
    tags = pos_tags_to_dict(token)
    return feature_set_from_dict(tags, upos)


def feature_set_from_dict(tags: dict[str, str], upos: UPOS) -> FeatureSet | None:
    """
    Maps a dictionary of features to a FeatureSet object.
    """
    if upos.is_noun_like():
        return NounFeatureSet(
            case=parse(tags.get("Case").upper(), Case),
            number=parse(tags.get("Number").upper(), Number),
            gender=parse(tags.get("Gender").upper(), Gender),
        )
    elif upos.is_verb_like():
        return VerbFeatureSet(
            tense=parse(tags.get("Tense").upper(), Tense),
            number=parse(tags.get("Number").upper(), Number),
            person=parse_person(tags.get("Person")),
        )
    return None


def parse[T](string: str, enum: EnumMeta) -> T:
    """
    Parses arbitrary spaCy token attribute string into specified enum.
    For example: parse("NOUN", UPOS) -> UPOS.NOUN
    """
    return enum.__members__.get(string)


def pos_tags_to_dict(token: SpacyToken) -> dict[str, str]:
    """
    Extracts a dict of features from the universal feature tags of a Token.
    :param token: A spaCy token with a token.morph string like "Case=Nom|Number=Plur"
    :return: The features, e.g. {'Case': 'Nom', 'Number': 'Plur'}
    """
    tags = str(token.morph).split("|")
    return {tag.split("=")[0]: tag.split("=")[1] for tag in tags if tag != ""}


def parse_person(person: str) -> Person:
    """
    Number is a special feature, as it is denoted with "1", "2" or "3" in spaCy,
    which does not make for a valid enum value, so we need to parse it separately.
    """
    match person:
        case "1":
            return Person.FIRST
        case "2":
            return Person.SECOND
        case "3":
            return Person.THIRD
        case _:
            raise ValueError(f"Invalid value for Person: {person}")
