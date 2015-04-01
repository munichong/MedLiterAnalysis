'''
Created on Mar 17, 2015

@author: Wang
'''
import pickle
from nltk import word_tokenize
from extend_known_grants import Grant, findRegexPattern
from parse_documents import remove_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            body = remove_tags(body[0]) # Some bodies which were not empty become empty here. The reason is the text between the body tags are HTML tags
                                        # e.g. J:\Medical Papers Data\articles.C-H\\Environ_Health_Perspect\Environ_Health_Perspect_1997_May_105(5)_514-520.nxml
            pub_body.append(body)
        else:
            pub_body.append(None)
            
    tfidfVectorizer.fit( [b for b in pub_body if b ] )
    
    for index, body in enumerate( pub_body ):
        if not body:
            grant.publications[index].vector = None
            continue
        vec = tfidfVectorizer.transform([body])
        grant.publications[index].vector = vec
        
    return grant

def initial_new_grant(grant_old, seeds):
    grant_new = Grant(grant_old.grantID)
    grant_new.authors_pool = grant_old.authors_pool
    for pub in seeds:
        grant_new.addPublication(pub)
    return grant_new

if __name__=='__main__':
    
    grant_withCandiPubs = pickle.load( open('../grantsWithCandiPubs.pkl', 'rb') ) # The pkl file is created in 'extend_known_grants'
    simi_threshold = 0.9
    
    n = 0
    grants_final = []
    for grant in grant_withCandiPubs:
        n += 1
        print("*** GRANT", n)
        print(len(grant.publications), "publications in this grant")
        grant = body_vector(grant)
        print(len( [ 1 for pub in grant.publications if pub.vector != None ] ), "publications have vectors")
        
        # find seed publications whcih have grant ID
        seed_vector = None
        num_of_seeds = 1
        pub_seeds = []
        for index, pub in enumerate( grant.publications ):
            if not pub.isSeed:
                continue
            if seed_vector == None:
                seed_vector = pub.vector
            else:
                seed_vector = seed_vector + pub.vector

                
            pub_seeds.append(pub)
            num_of_seeds += 1
        seed_vector /= num_of_seeds # compute the centroid of the seeds as the seed vector
        
        # compute pairwise distances
        similarity_to_seed = []
        for pub in grant.publications:
            if pub in pub_seeds or pub.vector == None:
                continue
            similarity = cosine_similarity( pub.vector, seed_vector )
#             print(similarity)
            similarity_to_seed.append( (pub, similarity[0][0]) )
        
        # truncate the similar pubs 
        similarity_to_seed = sorted( similarity_to_seed, key=lambda x:x[1], reverse=True )
        grant_new = initial_new_grant( grant, pub_seeds )
        for pub, simi in similarity_to_seed:
            if simi < simi_threshold:
                break
            grant_new.addPublication(pub)
        grants_final.append(grant_new)        
        print(len(grant_new.publications), "publications are recalled")
        print("***\n")

    # pickle grants_final
    pickle.dump( grants_final, open('../grants_final.pkl', 'wb') )
    
    
    