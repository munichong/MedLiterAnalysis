'''
Created on Jul 15, 2014

@author: munichong

After updating article_citations.csv, this module extracts unique journal names 
and append new journals to journal_impactfactor.csv
without overwriting the impact factors that have been found

'''
import csv
unique_journals = set()
""" Read all journals which are up-to-dated """
with open( '../article_citations.csv', 'r') as ac:
    ac = csv.reader( ac )
    for line in ac:
        journal = line[4].lower()
        unique_journals.add( journal )

""" Read all journals which have been processed before """
with open( '../journal_impactfactor.csv', 'r') as ji:
    ji = csv.reader( ji )
    for line in ji:
        journal = line[0].lower()
        if journal in unique_journals:
            unique_journals.discard( journal )

""" append new journals """
with open( '../journal_impactfactor.csv', 'a') as ji_new:    
    for jn in unique_journals:
        ji_new.write( '\n' + jn )
    
    