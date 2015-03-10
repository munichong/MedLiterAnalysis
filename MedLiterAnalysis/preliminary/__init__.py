# acknowledgement = "asknskjfadkjnasdlkjnfdsa(WER-23-123-23)kjakunasdkfnj"
# import re
# regex = "([A-Z]{3}\-[0-9]{2}\-[0-9]{3}\-[0-9]{2})"
# reg = re.compile( regex )
# match = reg.search( acknowledgement )
# print match.groups()
    
# 
# def findRegexPattern(regex, text):    
#     reg = re.compile( regex )
#     match = reg.search( text )
#     
#     if match == None:
#         return None
#     
#     return match.groups()
# 
# def remove_tags(text):    
#     """ remove any noisy tags in matching """
#     tags_re = re.compile( "<([\s\S]*?)>" )
#     match = tags_re.findall( text )
# #    print match
#     for m in match:
#         text = text.replace(m, "")
#     return text.replace("<>", " ").replace("</>", " ").replace("  ", " ").strip() 
#     
# # fdata = open( "/home/munichong/Desktop/Carbon_Balance_Manag_2009_Oct_29_4_9.nxml" , 'r').read()
# fdata = "<article-title xml:lang=\"en\">LETTER TO THE EDITOR</article-title>"
# article_title = findRegexPattern( "<article-title[]>([\s\S]*?)</article-title>", fdata )[0]
# print article_title
# print remove_tags( article_title )


# print compute_similarity("a b", "b f")
