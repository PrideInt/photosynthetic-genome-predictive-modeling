# So I want to expand my knowledge on predictive modeling as I'm not totally
# experienced on the subject.

# I know that I want to use some machine learning techniques and algorithms to
# statistically compute an (inputed?) prediction. I want to start using other
# classification algorithms plus preprocessing techniques, because all the
# data that I've been using have already been preprocessed.

# I've decided that I'll use data from UniProtKB. It's probably a lot of
# data that I'll have to dissect and I have little idea of where to begin,
# but I will attempt to utilize either principal component analysis (PCA) or
# t-SNE (t-distributed stochastic neighbor embedding) to preprocess and
# visualize the data prior to applying the classification algorithms,
# whichever is more appropriate, or another algorithm if neither works.

# I may also utilize feature selection. It's pretty good when analyzing
# genomic data.

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Classification algorithms I will/may use:
# - Naive Bayes
# - Logistic Regression
# - Support Vector Machine (SVM)
# - Random Forest
# - K-Nearest Neighbors (KNN)
# - Neural Network
# - Decision Tree

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

# Here, I'll access data from UnitProtKB.
# The following from the API queries help page.

import re
import requests
from requests.adapters import HTTPAdapter, Retry

re_next_link = re.compile(r'<(.+)>; rel="next"')
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        total = response.headers["x-total-results"]
        yield response, total
        batch_url = get_next_link(response.headers)

# A URL
url = ''
progress = 0
with open('.tsv', 'w') as f:
    for batch, total in get_batch(url):
        lines = batch.text.splitlines()
        if not progress:
            print(lines[0], file=f)
        for line in lines[1:]:
            print(line, file=f)
        progress += len(lines[1:])
        print(f'{progress} / {total}')

# I'll have to preprocess this data now.

# Here I'll train the model with the data.

# User input stuff here?