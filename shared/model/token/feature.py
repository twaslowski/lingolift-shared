from abc import ABC
from enum import Enum

from pydantic import BaseModel


class FeatureSet(ABC, BaseModel):
    """
    Replaces the previous Morphology class.
    This is a structured way of representing the Universal Features, which are contained as strings in spaCy tokens.
    This focuses specifically on a subset of features relevant to the German language.
    Reference: https://universaldependencies.org/u/feat/index.html
    """


class NounFeatureSet(FeatureSet):
    """
    Represents a set of features relevant to a noun or related words.
    Applied to NOUN, PRON, DET, ADJ.
    """

    case: "Case"
    gender: "Gender"
    number: "Number"


class VerbFeatureSet(FeatureSet):
    """
    Represents a set of features relevant to a verb or related words.
    Applied to VERB, AUX.
    """

    tense: "Tense"
    person: "Person"
    number: "Number"


class Feature(Enum):
    pass


class Case(Feature):
    NOM = "nominative"
    ACC = "accusative"
    DAT = "dative"
    GEN = "genitive"


class Gender(Feature):
    MASC = "masculine"
    FEM = "feminine"
    NEUT = "neuter"


class Number(Feature):
    SING = "singular"
    PLUR = "plural"


class Person(Feature):
    FIRST = "first person"
    SECOND = "second person"
    THIRD = "third person"


class Tense(Feature):
    PRES = "Present tense"
    PAST = "Past tense"
    IMP = "Imperfect"
    FUT = "Future tense"
    PQP = "Pluperfect"
