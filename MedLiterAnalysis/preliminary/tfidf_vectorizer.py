'''
Created on Mar 17, 2015

@author: Wang
'''
import pickle
from nltk import word_tokenize
from extend_known_grants import Publication, Grant, findRegexPattern
from parse_documents import extract_target_content, remove_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering


def body_vector(grant):
    tfidfVectorizer = TfidfVectorizer( stop_words='english', 
                                       tokenizer=word_tokenize, ngram_range=(1, 3), max_features=100 )
    root = "J:\\Medical Papers Data\\"
    pub_body = []
    for publication in grant.publications:
        file_path = root + publication.relative_path
        fdata = open(file_path, 'r').read()
        body = findRegexPattern( "<body[\s\S]*?>([\s\S]*?)</body>", fdata )
        
        if body:
            body = remove_tags(body[0])
            pub_body.append(body)
        else:
            pub_body.append(None)
    
    tfidfVectorizer.fit( [b for b in pub_body if b ] )
    
    b_vec = []
    for body in pub_body:
        if not body:
            b_vec.append(None)
            continue
        vec = tfidfVectorizer.transform([body])
        b_vec.append( vec )
    return b_vec

if __name__=='__main__':
    
    grant_withCandiPubs = pickle.load( open('../grantsWithCandiPubs.pkl', 'rb') ) # The pkl file is created in 'extend_known_grants'
    
    n = 0
    for grant in grant_withCandiPubs:
        n += 1
        print("*** GRANT", n)
        print(len(grant.publications), "publications in this grant")
        vectors = body_vector(grant)
        print(len(vectors), "publications have vectors")
        print("***\n")

    
    
    
    
    