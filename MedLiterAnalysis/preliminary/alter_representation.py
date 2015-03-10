'''
Created on Jul 15, 2014

@author: munichong
'''
import csv

def grant_cite_ifr():
    grant_dict = {}
    with open( '../article_cite_ifr.csv', 'r' ) as aci:
        aci = csv.reader( aci )
        for line in aci:
            grantNo = line[6]
            
            if not grant_dict.has_key( grantNo ):
                grant_dict[ grantNo ] = { 'citations':[], 'impact_factors':[] }
                
            impactFactor = line[5]
            citations = line[7]    
            grant_dict[ grantNo ][ 'citations' ].append( citations )
            grant_dict[ grantNo ][ 'impact_factors' ].append( impactFactor )
            
    with open( '../articleCiteIf.csv', 'w' ) as aci_new:
        aci_new = csv.writer( aci_new )
        for grantNo, info in grant_dict.items():
            combine = zip( info['citations'], info['impact_factors'] )
            output = [ grantNo ]
            for c, i in combine:
                string = 'Cited by: ' + c + '  Impact Factor: ' + i
                output.append( string )
            aci_new.writerow( output )
            

if __name__ == "__main__":
    grant_cite_ifr()
    