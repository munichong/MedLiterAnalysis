'''
Created on Mar 11, 2015

@author: Wang
'''
import csv, re, os, pickle
from parse_documents import extract_target_content

class Publication:
    def __init__(self, line):
        self.relative_path = "\\".join( [ line[0], line[1], line[2] ] )
        self.title = line[3]
        self.journal = line[4]
        self.authors = []
        self.pmid = ''
        self.isSeed = False
        
        if len(line) > 5:
            self.grantID = line[6]
            self.citation = line[7]
            self.isSeed = True
        
    def setAuthors(self, authors_list):
        self.authors = authors_list 
        
    def setPMID(self, pmid):
        if pmid:
            self.pmid = pmid
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.relative_path == other.relative_path
           

class Grant:
    def __init__(self, grantID):
        self.grantID = grantID
        self.authors_pool = set()
        self.publications = []
        
    def addPublication(self, pub):
        if pub not in self.publications:
            self.publications.append(pub)

    def addAuthors(self, authors):
        self.authors_pool.update(authors) # add all elements in a list to a set
        
    def has_author(self, author_name):
        return author_name in self.authors_pool


def findRegexPattern(regex, text):    
    reg = re.compile( regex )
    all_macthes = reg.findall( text )
    if not all_macthes:
        return None
    return all_macthes

def extract_authors(text):
    try:
        contrib_group = findRegexPattern( "<contrib-group([\s\S]*?)</contrib-group>", fdata )[0]
    #         print(rawfile_path)        
        """ extract author names """
        extracted_authors = findRegexPattern( "<name([\s\S]*?)</name>", contrib_group )
        cleaned_authors = []
        for author in extracted_authors:
            cleaned_authors.append( 
                                   author.replace("><surname>", "").replace("</surname><given-names>", ", ").replace("</given-names>", "")
                                   )
        return cleaned_authors    
        
    except TypeError:
        """ if the text does not contain "<contrib-group" or "<name" """
        return None

def match_authors(text):
    authors_list = extract_authors(text);
    if authors_list:
        grants = []
        for author in authors_list:    
            for grant in grant_table.values():
                if grant.has_author(author):
                    grants.append(grant)
        return grants
    return None

def create_publication_instance(folder, dirname, filename, fdata):
        
    """ For output """
    journal_title = extract_target_content( "<journal-title>([\s\S]*?)</journal-title>", fdata )
    if journal_title:
        journal_title = journal_title.lower()
#     print("JOURNAL-TITLE:", journal_title)
        
    """ <title-group> <article-title> </article-title> <subtitle> </subtitle> <title-group>  """
    article_title = extract_target_content( "<title-group[\s\S]*?>([\s\S]*?)</title-group>", fdata )
    if article_title:
        article_title = article_title.replace( "-", " " )
#     print("ARTICLE-TITLE:", article_title)

    publication = Publication([ folder, dirname, filename, article_title, journal_title ])
    publication.setAuthors( extract_authors(fdata) )
    publication.setPMID( extract_pmid(fdata) )
    return publication

def extract_pmid(fdata):
    pmid = extract_target_content( "<article-id pub-id-type=\"pmid\"([\s\S]*?)</article-id>", fdata )
    return pmid



if __name__ == '__main__':  
    """ Read seed grants """
    grant_table = {} # key: grantID, str   value: Grant instance
    print("Reading \"article_cite_ifr.csv\"...")
    with open("../article_cite_ifr.csv", 'r', encoding="utf8") as acifile:
        aci_reader = csv.reader(acifile)
        for newline in aci_reader:
            
            grantID = newline[6]
            publication = Publication(newline)
            
            """ add authors and create publication instance """
            rawfile_path = "J:\\Medical Papers Data\\" + "\\".join( [ newline[0], newline[1], newline[2] ] )
#             print(rawfile_path)
            fdata = open( rawfile_path, 'r' ).read()
            authors_list = extract_authors( fdata )
            publication.setAuthors( authors_list )
            publication.setPMID( extract_pmid(fdata) )
            
            """ add into grant_table """
            if grantID in grant_table:
                grant_table[grantID].addPublication( publication )
                grant_table[grantID].addAuthors( publication.authors )
            else:
                grant = Grant(grantID)
                grant.addPublication(publication)
                grant.addAuthors( publication.authors )
                grant_table[grantID] = grant
    print("Finish Reading\n    ---", len(grant_table), "known grants are extracted and created.")
    
    
    """ Find publications whose authors are also participate in seed grants. """
    root = "J:\\Medical Papers Data\\"
    folders = [ "articles.A-B\\", "articles.C-H\\", "articles.I-N\\", "articles.O-Z\\" ]  
    matched_pub_counter = 0 
    total_filenum = 0 
    for folder in folders:
        path = root + folder 
        print(folder) 
        dir_num = 0 
        for dirname in os.listdir( path ): 
            dir_num += 1
            print(folder, dirname, dir_num, matched_pub_counter, total_filenum)
            for filename in os.listdir( path + dirname ):
                if filename[0] == '#' and filename[-1] == '#':
                    continue
                total_filenum += 1
                fdata = open( path + dirname + '\\' + filename , 'r').read()
                
                """ Check if at least one author wrote any known grant. """
#                 print(path + dirname + '\\' + filename)
                matched_grants = match_authors(fdata)
                if not matched_grants:
                    continue
                
#                 print(dirname, "Find matched grants")
                
                """ If any author wrote any grant, create a publication instance and add into the grants. """
                publication = create_publication_instance(folder, dirname, filename, fdata)
                for grant in matched_grants:
                    grant.addPublication(publication)
                
#                 print("ADD PUB. TO", len(matched_grants), "grants:", folder + filename)
                matched_pub_counter += 1
            
    print(matched_pub_counter, "publications are matched.")
    
                
    """  """       
    grant_withCandiPubs = []
    for grant in grant_table.values():
        grant_withCandiPubs.append(grant)
    pickle.dump(grant_withCandiPubs, open('../grantsWithCandiPubs.pkl', 'wb'))            
            
            