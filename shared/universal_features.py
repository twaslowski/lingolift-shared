import json
import os


def load_feature_set() -> dict[str, dict[str, str]]:
    """
    Loads the feature set for a given language.
    :return: The feature set with mappings of Universal Feature tags to legible descriptions.
    """
    dirname = os.path.dirname(__file__)
    feature_set_de = os.path.join(dirname, "features/features_de.json")
    with open(feature_set_de) as f:
        return json.load(f)  # type: ignore


all_features = load_feature_set()
nominal_features = ["Case", "Number", "Gender"]
verbal_features = ["Person", "Number", "Tense"]


def get_all_feature_instances(feature: str) -> list[str]:
    """
    :param feature: The feature to get all instances for, e.g. "Case"
    :return: A list of all instances for the given feature, e.g. "Nom", "Acc", "Dat", "Gen"
    """
    return list(all_features.get(feature).keys())  # type: ignore


def convert_to_legible_tags(tags: dict, feature_set: list[str]) -> str:
    """
    Converts the Universal Feature tags to a legible format, e.g. "Case=Nom | Number=Plur | Gender=Masc"
    to "Nominative Plural Masculine".
    :param tags: key-value pairs of Universal Feature tags, e.g. {'Case': 'Nom', 'Number': 'Plur'}
    :param feature_set: The list of features to use, e.g. 'Case', 'Number', 'Gender'
    :return:
    """
    legible_tags = []
    for feature in feature_set:
        tag_value = tags.get(feature)
        if tag_value:
            legible_tags.append(all_features.get(feature).get(tag_value))  # type: ignore

    return " ".join(filter(lambda x: x is not None, legible_tags))  # type: ignore
