from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv

def query(query):
    csv_file = open('./records/record.csv', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')

    docs = []

    for row in reader:
        docs.append(row[6])

    vectorizer = TfidfVectorizer(lowercase=True)
    vectorizer.fit(docs)

    docs_tfidf = vectorizer.transform(docs)

    query_tfidf = vectorizer.transform([query])[0]

    cosines = []
    for d in docs_tfidf:
        cosines.append(float(cosine_similarity(d, query_tfidf)))

    sorted_ids = np.argsort(cosines)

    founded = 0
    for i in range(3):
        cur_id = sorted_ids[-i-1]
        if (cosines[cur_id] > 0):
            founded += 1
            print(docs[cur_id], cosines[cur_id])

    if (founded > 0):
        print(f"{founded} article found!")
    else:
        print("no match found!")
