from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from tqdm import tqdm
from doc2vec import load_model_d2v
from clean_data import ArticleCleaner
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
import logging
import json
import collections

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
#from sklearn.model_selection import GridSearchCV

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

root_path = Path.cwd()

# load the model to inferre the vectors in the annotated data set
model_path_d2v = os.path.join(root_path, "data", "d2v_models")
model = load_model_d2v("06-04-2020", model_path_d2v)

cleaner = ArticleCleaner()

files = ["data/extended_cleaned.jsonl"]
cleaned_text = []
labels = []

for filename in files:
    with open(filename, "r") as f:
        for line in tqdm(f.readlines()):
            line = json.loads(line)
            line["text"] = cleaner.clean(line["text"])
            cleaned_text.append(line["text"])
            labels.append(line["annotations"][0]["label"])

article_vectors = [model.infer_vector(text) for text in cleaned_text]
article_vectors = np.array(article_vectors)

X_train, X_test, y_train, y_test = train_test_split(
    article_vectors, labels, test_size=0.33, random_state=42
)
#hyperparameters descided via GridSearch
clf = svm.SVC(kernel="poly", class_weight="balanced", C = 1, degree=2, probability=True)
clf.fit(X_train, y_train)
print('svc', clf.score(X_test, y_test))

np.set_printoptions(precision=2)
disp = plot_confusion_matrix(clf, X_test, y_test, cmap=plt.cm.Blues)
plt.show()

#hyperparameters descided via GridSearch
clf2 = RandomForestClassifier(n_estimators=30, max_features='log2')
clf2.fit(X_train, y_train)
print('rf', clf2.score(X_test, y_test))

disp = plot_confusion_matrix(clf2, X_test, y_test, cmap=plt.cm.Blues)
plt.show()

eclf = VotingClassifier(
    estimators=[('svc', clf), ('rf', clf2)],
    voting='soft')

for clf, label in zip([clf, clf2, eclf], ['CVR', 'Random Forest', 'Ensemble']):
    scores = cross_val_score(clf, article_vectors, labels, scoring='accuracy', cv=5)
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

eclf.fit(X_train, y_train)

disp = plot_confusion_matrix(eclf, X_test, y_test, cmap=plt.cm.Blues)
plt.show()