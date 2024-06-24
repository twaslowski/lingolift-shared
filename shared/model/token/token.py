from __future__ import annotations

from pydantic import BaseModel

from shared.model.token.feature import FeatureSet
from shared.model.token.upos import UPOS


class Token(BaseModel):
    """
    This class represents a subset of a spacy.token.Token object.
    It is used to provide a more robust and structured representation of the token.
    """

    text: str
    lemma: str
    upos: UPOS
    feature_set: FeatureSet | None
    ancestor: Token | None = (
        None  # object reference; ids could arguably used in the same way spaCy does
    )
