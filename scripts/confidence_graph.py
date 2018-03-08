import matplotlib.pyplot as plt
import numpy as np
import random

from helpers.deep import get_processed_data
from helpers.common import classification_confidence


COLORS = [
    '#73926e',
    '#e6194b',
    '#3cb44b',
    '#ffe119',
    '#0082c8',
    '#f58231',
    '#911eb4',
    '#aaffc3',
    '#d2f53c',
    '#008080',
    '#e6beff',
    '#aa6e28',
    '#800000',
    '#808080',
]


def get_confidences(classifier):
    """
    Get the confidences values for all the datasets
    @classifier: classifier object

    It returns {correct_confidences: [float], incorrect_confidences:[float]}
    """
    deep_data = get_processed_data(
        '_playground/sample_data/processed_sectors_subsectors.csv'
    )
    # confidences for correct and incorrect prediction
    correct_confidences = []
    incorrect_confidences = []

    for text, label in deep_data[:100]:
        classification = classifier.classify_as_label_probs(text)
        confidence = classification_confidence(classification)
        classified_label = classification[0][0]  # get the max
        if classified_label == label:  # means correct confidence
            correct_confidences.append(confidence)
        else:
            incorrect_confidences.append(confidence)
    return {
        'correct_confidences': correct_confidences,
        'incorrect_confidences': incorrect_confidences
    }


def scatter_plot(confidences):
    fig = plt.figure(figsize=(15, 8))
    maxlen = max([len(x) for k, x in confidences.items()])
    for key, confs in confidences.items():
        color = COLORS[random.randrange(len(COLORS))]
        avg = np.mean(confs)
        # median = np.median(confs)
        plt.scatter(np.arange(len(confs)), confs, color=color, label=key)
        meanX = [x for x in range(maxlen)]
        meanY = [avg for _ in range(maxlen)]
        plt.plot(meanX, meanY, color=color, label=key+" mean")
    plt.legend()
    return fig