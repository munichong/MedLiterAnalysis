'''
Created on Jul 15, 2014

@author: munichong
'''
import csv

""" Read all journal:impactFactor into a dictionary """
impactFactors = {}
with open( '../journal_impactfactor.csv', 'r' ) as jif:
    jif = csv.reader( jif )
    for journal, ifr in jif:
        impactFactors[ journal.lower() ] = ifr
print "Impact factors have been read."


""" Insert impactFactors into article-citation """
output = []
with open( '../article_citations.csv', 'r' ) as ac:
    ac = csv.reader( ac )
    for line in ac:
        journal = line[4].lower()
        ifr = ''
        ifr = impactFactors.get( journal, '')
        line.insert( 5, ifr )
        output.append( line )
print "Impact Factors are inserted."


""" Output """
with open( '../article_cite_ifr.csv', 'w' ) as ac:
    ac = csv.writer( ac )
    for line in output:
        ac.writerow( line )
print "Output."
        
        
        
