import json
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from functools import wraps

#nltk.download("punkt")
#nltk.download("stopwords")


PIPELINE = []

nlp = nltk.data.load("tokenizers/punkt/danish.pickle")


class ArticleCleaner:
    def __init__(self):
        self.pipeline = PIPELINE
        self.sent_tokenizer = nlp

    def clean(self, text):
        for cleaner in self.pipeline:
            text = cleaner(text, sent_tokenizer=self.sent_tokenizer)
        return text


# create a pipeline of cleaning functions
# https://nlpforhackers.io/building-a-nlp-pipeline-in-nltk/
def add_to_pipeline(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res

    PIPELINE.append(wrapper)
    return wrapper


@add_to_pipeline
def fix_encoding(text: str, sent_tokenizer=nlp):
    text = str(text.encode("utf-8"), "utf-8")
    return text


@add_to_pipeline
def _clean_text(text, sent_tokenizer=nlp):
    """Performs invalid character removal and whitespace cleanup on text."""
    dk_stopwords = stopwords.words("danish")
    out = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # mapps all punctuation to None
    word_tokens = word_tokenize(out.lower())  # tokenizes into individual words
    word_tokens = [w for w in word_tokens if not w in dk_stopwords]

    return word_tokens


if __name__ == "__main__":
    cleaner = ArticleCleaner()

    files = []

    for filename in tqdm(files):
        data = []
        with open(filename, "r") as f:
            for line in f.readlines():
                data.append(json.loads(line))
        cleaned_data = []
        for jsonline in data:
            if len(jsonline["label"]) == 0:
                continue
            jsonline["text"] = cleaner.clean(jsonline["text"])
            cleaned_data.append(jsonline)

        with open(filename.split(".")[0] + "cleaned.jsonl", "w") as f:
            for line in cleaned_data:
                f.write(json.dumps(line))
                f.write("\n")
