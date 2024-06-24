import functools
from pysentimiento import create_analyzer

@functools.cache
def load_analyzer():
    return {
        "hate": create_analyzer(task="hate_speech", lang="en"),
        "sentiment": create_analyzer(task="sentiment", lang="en"),
        "emotion": create_analyzer(task="emotion", lang="en"),
    }