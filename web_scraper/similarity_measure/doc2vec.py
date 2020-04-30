from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
from pathlib import Path
import json
from clean_data import ArticleCleaner
from tqdm import tqdm
import logging

"""
Run the data through the cleaning pipeline
docs should be a flat list of the text from the documents

#Build a metric for scoring how similar articles are
#Build a "leade-board" of articles I like
#Compare any new article with all the articles in the "leader-board", and recommend only if similarity is high enough
"""
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

root_path = Path.cwd()


def save_model(model, date, model_path):
    model.save(os.path.join(model_path, f"{date}_d2v.pkl"))


def load_model_d2v(date, model_path):
    model = Doc2Vec.load(os.path.join(model_path, f"{date}_d2v.pkl"))
    return model


def train_model_d2v(date):

    cleaner = ArticleCleaner()

    files = ["data/dr_spider.jsonl"]
    cleaned_text = []

    for filename in files:
        with open(filename, "r") as f:
            for line in tqdm(f.readlines()):
                line = json.loads(line)
                line["text"] = cleaner.clean(line["text"])
                cleaned_text.append(line["text"])

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(cleaned_text)]

    model_path_d2v = os.path.join(root_path, "data", "d2v_models")

    model_d2v = Doc2Vec(vector_size=80, min_count=2, epochs=40)
    model_d2v.build_vocab(documents)


    # Train model
    model_d2v.train(
        documents, total_examples=model_d2v.corpus_count, epochs=model_d2v.epochs
    )

    save_model(model_d2v, date, model_path_d2v)
    return model_path_d2v, documents


if __name__ == "__main__":

    model_path_d2v, documents = train_model_d2v("06-04-2020")

    model = load_model_d2v("06-04-2020", model_path_d2v)

    inferred_vector = model.infer_vector(documents[0].words)

    print(inferred_vector)
    print(type(inferred_vector))
    

    # ranks = []
    # second_ranks = []
    # for doc_id in range(len(documents)):
    #     inferred_vector = model.infer_vector(documents[doc_id].words)
    #     sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    #     rank = [docid for docid, sim in sims].index(doc_id)
    #     ranks.append(rank)

    #     second_ranks.append(sims[1])

    # import collections

    # counter = collections.Counter(ranks)
    # print(counter)
