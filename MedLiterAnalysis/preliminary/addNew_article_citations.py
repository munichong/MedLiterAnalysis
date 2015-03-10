'''
Created on Jul 18, 2014

@author: munichong
'''
import csv

old_article_line = {}
with open( '../article_citations_old.csv', 'r' ) as aco:
    aco = csv.reader( aco )
    for line in aco:
        art_file = line[2]
        old_article_line[ art_file ] = line[6] + ',' + line[7]


output = []
with open( '../qualified_articles.csv', 'r' ) as qa:
    qa = csv.reader( qa )
    for line in qa:
        art_file = line[2]
        if old_article_line.has_key( art_file ):
            """ if this article is OLD """
            output.append( ','.join( line ) + ',' + old_article_line[ art_file ] )
        else: 
            """ if this article is NEW """   
            output.append( ','.join( line ) )
       
        
with open( '../article_citations.csv', 'w' ) as acn: 
    for line in output:
        acn.write( line + '\n' )
        