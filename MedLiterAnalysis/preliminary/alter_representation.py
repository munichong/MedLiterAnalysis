'''
Created on Jul 15, 2014

@author: munichong
'''
import csv, pickle
from extend_known_grants import Publication, Grant

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

def output_final_grants():
    grants_final = pickle.load( open('../grants_final.pkl', 'rb') )
    
    csv_writer = csv.writer( open('../grants_final.csv', 'w', encoding="utf8", newline='') )
    num_of_grant = 0
    for grant in grants_final:
        num_of_grant += 1
        print("Processing Grant", num_of_grant)
        
        row1 = [ grant.grantID ]
        for pub in grant.publications:
            row2 = [pub.relative_path, pub.title, pub.journal, " & ".join(pub.authors)]
            row2.append(pub.citation) if hasattr(pub, 'citation') else row2.append("")
            csv_writer.writerow(row1 + row2)
        
def statistics():
    csv_reader = csv.reader(open('../grants_final.csv', 'r', encoding='utf-8'))
    ans1 = {}
    for row in csv_reader:
        grantID = row[0]
        ans1[grantID] = ans1.get(grantID, 0) + 1
    ans2 = {}
    for grantID, pub_count in ans1.items():
        ans2[pub_count] = ans2.get(pub_count, 0) + 1
    print(ans2)
    
    
if __name__ == "__main__":
    statistics()
    