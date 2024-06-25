from typing import List, Union

from pydantic import BaseModel

"""
Deprecated, replaced by shared.model.token.Token
"""


class PartOfSpeech(BaseModel):
    value: str
    explanation: str


class Morphology(BaseModel):
    tags: dict[str, str]
    explanation: Union[str, None]

    def tags_to_string(self) -> str:
        return "|".join([f"{k}={v}" for k, v in self.tags.items()])

    def stringify_explanation(self) -> Union[str, None]:
        return self.explanation if self.explanation else None


class SyntacticalAnalysis(BaseModel):
    word: str
    pos: PartOfSpeech
    morphology: Union[Morphology, None]
    lemma: Union[str, None]
    dependency: Union[str, None]

    def stringify_lemma(self) -> str | None:
        return f" (from: {self.lemma})" if self.lemma else None

    def stringify_dependency(self) -> Union[str, None]:
        # Only return something IF there is a dependency AND the word is inflected in the first place
        return (
            f" (refers to: {self.dependency})"
            if self.dependency and self.lemma
            else None
        )

    def stringify(self) -> str:
        properties: List[str] = []
        add_property(properties, self.stringify_lemma())
        add_property(properties, self.stringify_dependency())
        add_property(properties, self.pos.explanation)
        if self.morphology:
            add_property(properties, self.morphology.stringify_explanation())
        # add_feature(features, self.dependency)
        return "; ".join(properties)


def add_property(features: list[str], feature: Union[str, None]) -> None:
    if feature:
        features.append(feature)
