'''
Created on Jul 12, 2014

@author: munichong
'''
import os, re
from html import entities
from xml.dom import minidom
import string

def unescape(text):
    """ This function converts HTML entities and character references to ordinary characters. """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def findRegexPattern(regex, text):    
    reg = re.compile( regex )
    match = reg.search( text )
    if match == None:
        return None
#     print match.groups()
    return match.groups()

def remove_tags(text):    
    """ remove any noisy tags in matching """
    tags_re = re.compile( "<([\s\S]*?)>" )
    match = tags_re.findall( text )
#    print match
    for m in match:
        text = text.replace(m, "")
    return unescape( text.replace("<>", " ").replace("</>", " ").replace("  ", " ").strip() )

def replace_unprintable(text, new_string):
    unpStr = ''
    for t in text[:]:
        if t in string.printable:
            if not unpStr == '':
                text = text.replace( unpStr, new_string )
                unpStr = ''
        else:
            unpStr += t
    return text

def is_valid_grantNo(gn):
    if any( x.isupper() for x in gn ) and any( x.isdigit() for x in gn ) and not any( x.islower() for x in gn):
        return True
    else:
        return False
 
def extract_grantNo(text):
    
    """ If being granted by ACS, check whether target content has Grant No. (two possible formats) """
    grantNo_long = findRegexPattern( "([A-Z]{2,5}[\- ][0-9]{2}\-[0-9]{3}\-[0-9]{2}\-[A-Z]{2,5})", 
                                            text )    # REG-03-098-08-EFS
    
    grantNo_endPara = findRegexPattern( "([A-Z]{2,5}[\- ][0-9]{2}\-[0-9]{3}\-[0-9]{2}[\s]{0,1}\([A-Z]{2,5}\))",
                                            text )    # REG-03-098-08(EFS) or REG-03-098-08 (EFS)
    
    grantNo_short = findRegexPattern( "([A-Z]{2,5}[\- ][0-9]{2}\-[0-9]{3}\-[0-9]{2})", 
                                            text )    # REG-03-098-08
    
#     grantNo_compact = findRegexPattern( "([A-Z]{2,5}[0-9]{7}[A-Z]{0,5})", text )    # REG0309808
    
    grantNo_fullPara = findRegexPattern( "(American Cancer Society \([\s\S]*?\))", text )
    if not grantNo_fullPara:
        grantNo_fullPara = findRegexPattern( "(American Cancer Society grant \([\s\S]*?\))", text )
        if not grantNo_fullPara:
            grantNo_fullPara = findRegexPattern( "(ACS grant \([\s\S]*?\))", text )
    
    grantNo = ''
    """ First go with grantNo_long, if it is None, then go with grantNo_para which may also be None """
    if grantNo_long:
        grantNo = grantNo_long
    elif grantNo_endPara:
        grantNo = grantNo_endPara
    elif grantNo_short:
        grantNo = grantNo_short
#     elif grantNo_compact:
#         grantNo = grantNo_compact
    elif grantNo_fullPara:
        """ if grantNo_fullPara does NOT contain digits, DISCARD """
        grantNo_fullPara = [ x for x in grantNo_fullPara if re.compile('\d').search(x) ]
        grantNo = [ x[ x.index('(') + 1 : x.index(')') ] for x in grantNo_fullPara ]
    else:
        return None

    
    grantNo = [ replace_unprintable( gn, '-' ) for gn in grantNo  ]
#     for gn in grantNo[:]:
#         if not is_valid_grantNo( gn ):
#             grantNo.remove( gn )
           
    if len(grantNo) == 1:
        return grantNo[0]
    else:
        return "&".join( grantNo )

def extract_target_content(regex, text):
    target_content = findRegexPattern( regex, text )[0] # Get the first 
    target_content = remove_tags( target_content )
#     target_content = filter( lambda x: x in string.printable, target_content )
    target_content = replace_unprintable( target_content, "" )
    return target_content.replace("  ", " ")


root = "J:\\Medical Papers Data\\"
folder = "articles.A-B\\" # articles.A-B , articles.C-H , articles.I-N , articles.O-Z
path =  root + folder
output = []

# visit = {}
for dirname in os.listdir( path ):
#     visit[dirname] = 0
#     if dirname != "Oncogene":
#         continue
    print "\n******", path + dirname
    for filename in os.listdir( path + dirname ):
#         visit[dirname] += 1
#         if filename != "Oncogene_2012_Sep_6_31(36)_4045-4053.nxml":
#             continue
        print dirname + filename
        if filename[0] == '#' and filename[-1] == '#':
            continue
        
        fdata = open( path + dirname + '\\' + filename , 'r').read()
        
        acknowledgement = findRegexPattern( "<ack[\s\S]*?>([\s\S]*?)</ack>", fdata )
        abstract = findRegexPattern( "<abstract[\s\S]*?>([\s\S]*?)</abstract>", fdata )
        grantNo = ''
        """ whether the article has ACK and ABS """
        target_content = ''
        if acknowledgement == None and abstract == None:
            print "NO ACKNOWLEDGEMENT AND ABSTRACT FOUND!"
            continue
        elif acknowledgement != None and abstract != None:
            target_content = acknowledgement[0] + " " + abstract[0]
        else:
            """ acknowledgement == None or abstract == None (not both or neither) """
            target_content = acknowledgement[0] if abstract == None else abstract[0]
        
        
        
        target_content = remove_tags( target_content )
#         print "TARGET CONTENT:", target_content
        has_ACS_full = False
        has_ACS_abbr = False
        if ( "American Cancer Society" in target_content or 
             "American cancer society" in target_content or
             "american cancer society" in target_content ):
            has_ACS_full = True
        elif " ACS " in target_content:
            has_ACS_abbr = True
        
        has_grantNo = False
        grantNo = extract_grantNo( target_content )
        if grantNo:
            has_grantNo = True
        
        if not ( ( has_ACS_full or has_ACS_abbr ) and has_grantNo ):
            continue
        
        
        """ For output """
        journal_title = extract_target_content( "<journal-title>([\s\S]*?)</journal-title>", fdata )
        journal_title = journal_title.lower()
        print "JOURNAL-TITLE:", journal_title
        
        """ <title-group> <article-title> </article-title> <subtitle> </subtitle> <title-group>  """
        article_title = extract_target_content( "<title-group[\s\S]*?>([\s\S]*?)</title-group>", fdata )
        article_title = article_title.replace( "-", " " )
        print "ARTICLE-TITLE:", article_title
        
        
        this_output = [ folder, dirname, filename, article_title, journal_title, grantNo ]
        output.append( this_output )
        
        print ""

# print output

# for dir, n in visit.items():
#     print dir, n

with open("../qualified_articles_raw.csv", "a") as outfile:
    for line in output:
        line = [ s.replace(",", " ").replace(";", " ").replace("\n", " ").replace("\t", " ") for s in line ]
        outfile.write( ','.join( line ) + '\n' )       
outfile.close()    
print "\n", len(output), "qualified articles have been output!"    




    