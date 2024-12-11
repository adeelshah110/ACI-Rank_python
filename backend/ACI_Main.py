#change
import ACI 
import sys
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib64/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/titler/mt/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/packages/')
from collections import defaultdict 
import re 
from nltk.corpus import stopwords
import numpy as np
import lxml
import math
import quandl
import urllib
import nltk
import quandl
import numpy as np
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import pandas as pd 
import math
import textwrap
import sys
import re 
from nltk.corpus import stopwords
import numpy as np
import nltk
import urllib
from bs4 import BeautifulSoup
import numpy as np
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import pandas as pd 
import math
import textwrap
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import defaultdict,Counter
sys.path.insert(0, '/home/tko/himat/web-docs/keywordextraction')

from flask import Flask
import requests
from bs4 import BeautifulSoup
import numpy as np

sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')

sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')

common_nouns ="january debt est dec big than who use jun jan feb mar apr may jul agust dec oct nov sep dec  product continue one two three four five please thanks find helpful week job experience women girl apology read show eve  knowledge benefit appointment street way staff salon discount gift cost thing world close party love letters rewards offers special close  page week dollars voucher gifts vouchers welcome therefore march nights need name pleasure show sisters thank menu today always time needs welcome march february april may june jully aguast september october november december day year month minute second secodns".split(" ")
# especial characters
spchars = re.compile('\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\+|\=|\\|\||\{|\[|\]|\}|\:|\;|\'|\"|\<|\,|\>|\?|\/|\.|\-')

#stopwords list
#english_stopwords=set(stopwords.words("english"))




##########################################################################################################
def Clean_text(text,Stopword_List):
    Words =[]
    for word in text.split():       
        word = word.replace("’",' ')
        word = word.lower()
        word = spchars.sub(" ",word.strip())
        if word not in Stopword_List:
            if word not in common_nouns:
                if len(word)>1:

                    if word != "  ":
                        if word not in common_nouns:
                            if not word.isdigit():
                                if word not in Stopword_List:
                                    for x in word.split():
                                        if x not in Stopword_List and x not in common_nouns and len(x)>1 and x not in common_nouns:
                                            x = x.strip()
                                            if not x[0].isdigit():                                        
                                                    



                                                Words.append(x)                                  

    return (Words)
###################################################################################################################              
                  
# Input read from the txt file 
file_open = open ('read_write/input.txt','r')
url = file_open.readline()
file_open.close()
#####################################################################################
def writing_keywords(Score):
    sorted_score = Counter(Score)
    with open ('read_write/keyphrase.txt','w',encoding='utf-8') as kws:
        for i,x in sorted_score.most_common(10):
            kws.write(str(i)+'\n')
      

###########################################################
def Drank(url):
    # open thre text files 

    

    Score_for_word = defaultdict() # single word with score in dictionary form

    # Get text of the web page and HTM using beautiful soup
    Text,HTML = ACI.Web(url)  
    Txt_lang,Stopword_List=ACI .detect_language(Text)

    #divide the url into host and query parts
    url_host, url_query = ACI.Urls(url) 

    #Header,anchor,title text in the list 

    H1, H2, H3, H4, H5, H6, anchor, title = ACI.Extract_headerAnchorTitle(HTML)

    #process the text clean structure,tokenize,Remove:1-stopwords,2-length one words,3-common nouns 4-Blanks 5-Especial characters 6-numbers 7-symbols 
          
    words =Clean_text(Text,Stopword_List)          

    #calculate the length of candidate words          
    text_length =len(words)      
    # word and their frequency in the dictionary object
    words_and_freq = ACI.Calc_word_frequency(words) 
    
    
    headers_list =np.array([H1, H2, H3, H4, H5, H6, anchor, title,url_host,url_query])
    headers_name =np.array(['H1', 'H2', 'H3','H4', 'H5', 'H6', 'A', 'Title','URL-H','URL-Q'])
    score_headers =np.array([6, 5, 4,3, 2, 2, 1, 5,5,4])
    
    wrd_fr_Tgs_Fnl_score =defaultdict()
    Word_Final_Score =defaultdict()



    for word,fr in words_and_freq.items():
        tf_score = ACI.Tf_Score(fr,text_length)
        tag =[]
        name_tag =[]
         
        for v in range (len(headers_list)):
            if word in headers_list[v]:                            
                
                tag.append(score_headers[v]) 
                name_tag.append(headers_name[v])

        score= (sum(tag))
        score = score + tf_score

        Word_Final_Score[word] = score

        wrd_fr_Tgs_Fnl_score[word] =fr,name_tag,score
    return(Text, wrd_fr_Tgs_Fnl_score, Word_Final_Score,Txt_lang)
   


   
    
##################################################################
(Text, wrd_fr_Tgs_Fnl_score, Word_Final_Score,Txt_lang)= Drank(url)

#####################################################################
# Text.txt = write complete text for the webpage 
#Keyword : Write the Keywords Drank 
#Score : word-Frequency-tags and final Score
########################################################################
def Write(Text):
    words =' '
    for x in Text.split():        
        text = ''.join (x)        
        words += text+' '        
    return (words)
def Write_Text(Text,Txt_lang):    
    text_words =Write(Text)           
    good_text =textwrap.fill(text_words,140)    
    k =open('read_write/text.txt','w', encoding="utf-8")
    k.write('Language of the text is:'+Txt_lang +'\n'+'\n')
    
    k.write(str(good_text))    
    k.close()
###################################################################
Write_Text(Text,Txt_lang)
##############################################################
def Write_Keywords_txt(Word_Final_Score):
    with open ('read_write/keyphrase.txt','w',encoding='utf-8')as txt_keyword:
        txt_keyword.write('Keywords for the webpage'+'\n'+'\n')
        sorted_word_score = Counter(Word_Final_Score)
        for word,score in sorted_word_score.most_common(10):
            txt_keyword.write(str(word)+'\n')
            
#####################################################################
Write_Keywords_txt(Word_Final_Score)
##################################################################
def Write_Score_txt(wrd_fr_Tgs_Fnl_score):
    with open ('read_write/feature.txt','w',encoding="utf-8")as f:
        from prettytable import PrettyTable
        T_count =PrettyTable(["Word","Frequency",'TAGS','Final-Score'])    
        for x,i in wrd_fr_Tgs_Fnl_score.items():   
            T_count.add_row([x,i[0],i[1],i[2]])    
        f.write(str(T_count))
#############################################################################
Write_Score_txt(wrd_fr_Tgs_Fnl_score)
################################################################################