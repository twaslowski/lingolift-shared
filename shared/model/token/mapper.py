from enum import Enum, EnumMeta
from typing import TypeVar

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


def from_spacy_token(token: SpacyToken) -> LLToken:
    """
    Converts a spaCy token to a more structured Token object.
    """
    return LLToken(
        upos=map_upos(token),
        feature_set=map_features(token),
    )


def map_upos(token: SpacyToken) -> UPOS:
    """
    Maps a UPOS string from spaCy to the UPOS enum.
    """
    return parse(token.pos_, UPOS)


def map_features(token: SpacyToken) -> FeatureSet | None:
    upos = map_upos(token)
    tags = pos_tags_to_dict(token)
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
