from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv
from pprint import pprint

noise_amp = []
csv_file = open('./1400.csv', encoding='utf-8')
reader = csv.reader(csv_file, delimiter=',')

docs = []

for row in reader:
    docs.append(row[6])

# pprint(docs)


vectorizer = TfidfVectorizer(lowercase=True)
vectorizer.fit(docs)

# pprint(vectorizer.vocabulary_)

docs_tfidf = vectorizer.transform(docs)

# type(docs_tfidf), docs_tfidf.shape

# pprint(docs_tfidf)

# print (docs_tfidf.shape, len(vectorizer.vocabulary_))

# print(list(vectorizer.vocabulary_.keys())[:10])

query = 'پرونده مادی'

query_tfidf = vectorizer.transform([query])[0]

print(vectorizer.transform([query]))

cosines = []
for d in docs_tfidf:
    cosines.append(float(cosine_similarity(d, query_tfidf)))
    
sorted_ids = np.argsort(cosines)

# pprint(sorted_ids)

for i in range(1):
  cur_id = sorted_ids[-i-1]
  print(docs[cur_id], cosines[cur_id])