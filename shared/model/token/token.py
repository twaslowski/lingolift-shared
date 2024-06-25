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
    feature_set: FeatureSet | None = None
    ancestor: Token | None = (
        None  # object reference; ids could arguably used in the same way spaCy does
    )

    def __str__(self):
        result = []
        if self.text != self.lemma:
            result.append(f"(from: {self.lemma})")
        if self.ancestor:
            result.append(f" refers to: {self.ancestor.text}")
        result.append(f"{self.upos.value.capitalize()}")
        if self.feature_set:
            result.append(self.feature_set.__str__())
        return "; ".join(result)
