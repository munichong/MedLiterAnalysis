'''
Created on Mar 11, 2015

@author: Wang
'''
import csv, re, os

class Publication:
    def __init__(self, line):
        self.relative_path = "\\".join( [ line[0], line[1], line[2] ] )
        self.title = line[3]
        self.journal = line[4]
        self.grantID = line[6]
        self.citation = line[7]
        
    def setAuthors(self, authors_list):
        self.authors = authors_list    

class Grant:
    def __init__(self, grantID):
        self.grantID = grantID
        self.authors_pool = set()
        self.publications = []
        
    def addPublication(self, pub):
        self.publications.append(pub)
    
    def has_author(self, author_name):
        if author_name in self.authors_pool:
            return True
        return False


def findRegexPattern(regex, text):    
    reg = re.compile( regex )
    all_macthes = reg.findall( text )
    if all_macthes == None:
        return None
    return all_macthes

def extract_authors(text):
    contrib_group = findRegexPattern( "<contrib-group>([\s\S]*?)</contrib-group>", fdata )[0]
#         print(rawfile_path)        
    # extract author names
    return findRegexPattern( "<name>([\s\S]*?)</name>", contrib_group )


grant_table = {} # key: grantID, str   value: Grant instance
with open("../article_cite_ifr.csv", 'r', encoding="utf8") as acifile:
    aci_reader = csv.reader(acifile)
    for newline in aci_reader:
        
        grantID = newline[6]
        publication = Publication(newline)
        
        # add authors and create publication instance
        rawfile_path = "J:\\Medical Papers Data\\" + "\\".join( [ newline[0], newline[1], newline[2] ] )
        fdata = open( rawfile_path, 'r' ).read()
        authors_list = extract_authors( fdata )
        publication.setAuthors( authors_list )
        
        # add into grant_table
        if grantID in grant_table:
            grant_table[grantID].addPublication( publication )
        else:
            grant = Grant(grantID)
            grant.addPublication(publication)
            grant_table[grantID] = grant

            
root = "J:\\Medical Papers Data\\"
folders = [ "articles.A-B\\", "articles.C-H\\", "articles.I-N\\", "articles.O-Z\\" ]

for folder in folders:
    path = root + folder
    print "\n******", path   
    for dirname in os.listdir( path ):   
        for filename in os.listdir( path + dirname ):
            
        