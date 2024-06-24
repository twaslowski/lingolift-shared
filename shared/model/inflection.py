from typing import Union

from pydantic import BaseModel

from shared.model.syntactical_analysis import PartOfSpeech


class Inflection(BaseModel):
    """
    Represents an inflected word alongside information on its inflection.
    For example, "gehst" alongside "Person=2 Number=1 Tense=Pres" (as dict).
    """

    word: str
    morphology: dict[str, str]


class Inflections(BaseModel):
    """
    Represents a list of possible inflections for a given word.
    Additionally contains meta-information on that list of inflections, specifically whether it is a noun or a verb
    and its Gender, if applicable.
    """

    pos: PartOfSpeech
    gender: Union[str, None]  # for nouns only
    inflections: list[Inflection]
