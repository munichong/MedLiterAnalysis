'''
Created on Jul 14, 2014

@author: munichong
'''
import csv
import scholar

def get_finished_articles():
    outfile = open('../article_citations.csv', 'r')
    finished_articles = set()
    for line in csv.reader( outfile ):
        article_title = line[3]
        finished_articles.add( article_title )
    outfile.close()
    return finished_articles

def output(string):
    outfile = open('../article_citations.csv', 'a')
    outfile.write( string + '\n' )
    outfile.close()



with open('../qualified_articles.csv', 'r') as articles:
    finished_articles = get_finished_articles()
#     n=0
    for line in csv.reader( articles ):
        article_title = line[3]
#         n+=1
#         print n
        if article_title in finished_articles:
            continue
        
        """ retrieve citations from Google Scholar """
        citations, result_title = scholar.main( article_title )
        if not result_title:
            output_line = ','.join( line )
        else:
            output_line = ','.join( line ) + ',' + citations + ',' + result_title            
        output( output_line )
        