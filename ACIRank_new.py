# Imports
import urllib
import nltk
import sys
import re 

import lxml
import math
import string
import textwrap
import requests

from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import defaultdict,Counter
from nltk.corpus import stopwords
from collections import defaultdict 
from bs4.element import Comment
Common_Nouns ="january debt est dec big than who use jun jan feb mar apr may jul agust dec oct ".split(" ")
URL_CommnWords =['','https','www','com','-','php','pk','fi','http:','http']
URL_CommonQueryWords = ['','https','www','com','-','php','pk','fi','https:','http','http:']
UselessTagsText =['html','style', 'script', 'head',  '[document]','img']
from nltk import wordpunct_tokenize
from urllib.parse import urlparse 


warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 
warnings.filterwarnings("ignore")
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("finnish")
# Stopwords imports
from nltk.corpus import stopwords
STP_SET_ENG_NLTK = set(stopwords.words("english"))
F_stopwords = set(stopwords.words("Finnish"))
english_stop_words =[x for x in STP_SET_ENG_NLTK]
finnish_stop_words =[x for x in F_stopwords]
Eng_Finn_Combine_Stpwrds = english_stop_words + finnish_stop_words
############################################################################

# New imports
def Scrapper1(element):
    if element.parent.name in [UselessTagsText]:
        return False
    if isinstance(element, Comment):
        return False
    return True

def Scrapper2(body):             
    soup = BeautifulSoup(body, 'lxml')      
    texts = soup.findAll(text=True)   
    name =soup.findAll(name=True) 
    visible_texts = filter(Scrapper1,texts)        
    return u" ".join(t.strip() for t in visible_texts)

def Scrapper3(text):                  
    lines = (line.strip() for line in text.splitlines())    
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return u'\n'.join(chunk for chunk in chunks if chunk)


def Scrapper_title_4(URL):
  req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()
  title=[]
  
  soup = BeautifulSoup(html, 'lxml') 
  title.append(soup.title.string)
  return(title,urls)

def Web_Funtion(URL):
  req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()  
  Raw_HTML_Soup = BeautifulSoup(html, 'lxml') 
 
  raw =Scrapper2(html)
  Raw_text = Scrapper3(raw) 
  return(Raw_text,Raw_HTML_Soup) 

##################################################################
def Clean_NoSyn(No_syn):
    Words =[]
    for x in No_syn:
        x = x.strip('.').strip(':').strip('?').strip('/').strip("'").strip ("©").strip("»").strip("/").strip(" ").strip(",")
        for n in x.split('.'):
            for k in n.split('-'):
                for m in k.split('/'):
                    if m not in ["©","»","/"," "] and len(m)>1 and m.isalpha():
                        Words.append(m)
    return (Words)

def explode(h_d):
    alt_words=[]
    if len(h_d)>0:
        for k,i in h_d.items():      
   
            for x in i:
                word=[n for n in x.split(',')]
                for x in word:
                    words=[i for i in x.split() ]
                    for x in words:
                        alt_words.append(x)
        return(alt_words)
    else:
        return(alt_words)
    
def get_text(soup,h):
    text=[]
    zero=[]
    for w in soup.find_all(h):
        h_text = w.text.strip()
        h_text =h_text.replace(':','') #change made here
        h_text =h_text.replace(',','')
        
        #h_text =(h_text.lower())
        #change made here 
        for x in h_text.split('-'):
            text.append(x)
    if len(text)!=0:
        return(text)
    else:
        return(zero)
    
def Extract_headerAnchorTitle(soup):
    h1_d ={}
    h2_d ={}
    h3_d ={}
    h4_d ={}
    h5_d ={}
    h6_d ={}
    title_d={}
    
    h1_d['h1']= get_text(soup,'h1')
    h2_d['h2']= get_text(soup,'h2')
    h3_d['h3']=get_text(soup,'h3') 
      
    title_d['title']= get_text(soup,'title')  #CALLing      
    H1=explode(h1_d)
    H2=explode(h2_d)
    H3=explode(h3_d)
    

    
    T= explode(title_d)
    return(H1,H2,H3,T)


def Bold_italic_text(HTML):    
    bold_italic_text2 =[]
    bold = [w.text for w in HTML.find_all('bold')]
    italic = [w.text for w in HTML.find_all('i')]
    bold2 = [w.text for w in HTML.find_all('b')]
    strong  =bold2 = [w.text for w in HTML.find_all('strong')]
    bold_italic_text = bold + italic + strong
    for x in bold_italic_text:
        x = x.split()
        for i in x:
            bold_italic_text2.append(i)         
                   
    return (bold_italic_text2)

def Bold_italic_Score(feature,score,Upper,Capital,Stpwords_list):
    feature_dic ={}
    if len(feature)> 0: 
        feature =[x for x in feature if x not in Stpwords_list ]
        
        if Upper is True:
            list_bold = [x for x in feature if len (x) >1 and x[0].isupper() and not x[1].isupper()]
        if Capital is True:
            list_bold = [x for x in feature if len (x)>1 and x.isupper() ]
            
            
        
        len_f = len(feature)
        Counters = Counter (list_bold)
        for x,i in Counters.most_common():
            v = (i /len_f) *score
            feature_dic[x.lower()]=v
            
            
    return (feature_dic)  

def Get_Nosynsets(Text):
    no_syn_words =[]
    for i in Text.split():
        
        a1 =wn.synsets(i)
        
        if (len(a1))<1:
            
            if i not in STP_SET_ENG_NLTK and len(i)>1:
                
                no_syn_words.append(i.lower())
    
   
   
    Words = Clean_NoSyn(no_syn_words)
   
    return (Words)


def Score_feature(feature,score,stopwords_list):
    feature_dic ={}
    U_first = Bold_italic_Score(feature,2,True,False,stopwords_list)
    C_all= Bold_italic_Score(feature,3,False,True,stopwords_list)    
    
    if len(feature)> 0:   
        Score =0
        feature = [x for x in feature if x not in stopwords_list]
        len_f = int(len(feature))
        
        Counter_feature = Counter(feature)
        
        for x, i in Counter_feature.most_common():
            
            v = (i /len_f) *score
            U = U_first.get(x)
            C = C_all.get(x)
            Score = v
            #if C is not None:
                #Score += C
            #if U is not None:
                #Score += U
                
            
            feature_dic[x.lower()]=Score
    else:
        return (feature_dic)
    return (feature_dic)

def Check_null(word, feature_dict):
     m1 = feature_dict.get(word)
     if m1 is None:
         m1 = 0
     return (m1)
def Check_value(word,h1,h2,h3,host,Query,Title):
    m1 = Check_null(word, h1)
    m2 = Check_null(word, h2)
    m3 = Check_null(word, h3)    
    
    m4 = Check_null(word, host)
    m5 = Check_null(word, Query)
    m6 = Check_null(word, Title)  
    return (m1,m2,m3,m4,m5,m6)
def Get_Nouns_without_Stopwords(Text):
    Nouns =[]
    for line in Text.split():
       
        
        tokens = nltk.word_tokenize(line)
        
        tagged = nltk.pos_tag(tokens)    
        for x,y in tagged:
          if y in ['NNP','NNPS','NNS','NN']:
              #Nouns.append(x)
              if x not in STP_SET_ENG_NLTK:
                  Nouns.append(x)                
    return (Nouns)
def Function_ParseURL(URL):
    URL =str(URL)
    host=[]
    obj=urlparse(URL)    
    name =(obj.hostname)
    if len(name)>0:
        for x in name.split('.'):
            if x.lower() not in URL_CommonQueryWords:
                host.append(x)
        else:
            host.append(name)
    path=[]
    host_part_URL =[]
          
    for url_parts in URL.split('/'):
        for url_part in url_parts.split('.'):            
            if (len(url_part)>0):
                for url_words in url_part.split('-'):
                    if url_words.lower() not in URL_CommnWords and url_words.lower() not in host: 
                        path.append(url_words.lower())
            else:
                path.append(url_parts)                
    return(host,path)


def Frequent_Words(Text):
     
    #1 Remove stopwords and pre-process
    Cand_Words = [x for x in Text.split() if x not in Eng_Finn_Combine_Stpwrds]
    Cand_Words= Clean_NoSyn( Cand_Words)
    Cand_Words = [x.strip().lower() for x in Cand_Words if x not in ["©","»","/"," "] and len(x)>1 and x.isalpha()]
       
    #4 Counting freuqencies of candidate words
    Cand_100_Words_list =[]
    lengt_text = len(Cand_100_Words_list) 
    Count_Cand_Words = Counter(Cand_Words)
    Top_10_keywords=[]
    for word,count in Count_Cand_Words.most_common(10):
        Top_10_keywords.append(word)
    return (Top_10_keywords)


def Generate_100_Candidate_Keywords(URL,Text, HTML,STEMS):
    
    #1 Remove stopwords and pre-process
    Cand_Words = [x for x in Text.split() if x not in Eng_Finn_Combine_Stpwrds]
    Cand_Words= Clean_NoSyn( Cand_Words)
    Cand_Words = [x.strip().lower() for x in Cand_Words if x not in ["©","»","/"," "] and len(x)>1 and x.isalpha()]
    

    
    #4 Counting freuqencies of candidate words
    Cand_100_Words_list =[]
    lengt_text = len(Cand_100_Words_list) 
    Count_Cand_Words = Counter(Cand_Words)
    for word,count in Count_Cand_Words.most_common(100):        
        
        if STEMS:
            Cand_100_Words_list.append (stemmer.stem(word))
        else:
            Cand_100_Words_list.append(word)
        
    return (Cand_100_Words_list)

def Extract_keywords_Base(URL,Text, HTML, N):
    #Base method only make all false
    STEMS =False        
    Cand_100_Words_list = Generate_100_Candidate_Keywords(URL,Text, HTML,STEMS)    
        #2 Features URL list
    url_host, url_query = Function_ParseURL(URL)
    url_query = [x.strip().lower() for x in url_query if x not in ["©","»","/"," "] and len(x)>1 and x.isalpha()]
    
    #3 Feature Headers and title list
    H1, H2, H3,title = Extract_headerAnchorTitle(HTML)
    bold_italic = Bold_italic_text(HTML)
    bold_italic = Clean_NoSyn(bold_italic)
        
    #5 Score to the base Features(6) words
       
    h1 = Score_feature(H1,4,Eng_Finn_Combine_Stpwrds)
    h2 = Score_feature (H2,3,Eng_Finn_Combine_Stpwrds)
    h3 = Score_feature(H3,2,Eng_Finn_Combine_Stpwrds)     
    host =Score_feature(url_host,4,Eng_Finn_Combine_Stpwrds)
    Query = Score_feature (url_query,4,Eng_Finn_Combine_Stpwrds)
    Title = Score_feature (title,4,Eng_Finn_Combine_Stpwrds)
    Bold = Score_feature(bold_italic,2,Eng_Finn_Combine_Stpwrds)
    
    #6 Go through all the 100 candidate 100 words
    Cand_Words_Score_dic ={}
    
    for cand_word in Cand_100_Words_list:
        
        #7 Check_values for null if not null score for cand words
        H1_Score ,H2_Score ,H3_Score,URL_Host_Score,URL_Query_Score,Title_Score = Check_value(cand_word,h1,h2,h3,host,Query,Title)#no_syn_words,B)
        Final_feature_Score0 = round (H1_Score + H2_Score + H3_Score)
        Final_feature_Score1 = round (H1_Score + URL_Host_Score + Title_Score)
        Final_feature_Score2 = round (H1_Score + URL_Host_Score + Title_Score + URL_Query_Score)
        Final_feature_Score3 = round (URL_Host_Score + Title_Score + URL_Query_Score)
        Final_feature_Score4 = round (H1_Score + H2_Score + H3_Score + URL_Host_Score + URL_Query_Score + Title_Score , 2)
            
       
        #9 Store all cand 100 words and their features scores in dictionary        
       
        
        Cand_Words_Score_dic[cand_word] =   Final_feature_Score1
  
    
    
    #10 Counts the dictinary to get top 10 words
    Counts_Final_Features_Scores = Counter(Cand_Words_Score_dic)
    keywords =[]
    # 11 set number of keywords in case of mopsi 5
    Number_of_keywords = 10
        
    
    for word, fr in Counts_Final_Features_Scores.most_common(Number_of_keywords):
        keywords.append(word)
    
    
    #11 return the keywords for base method
        
    return (keywords)   
    
###########################################################################
def Score_in_Feature(candidate_word,feature_score_dic):
    New_feature_dic ={}
    for word in candidate_word:
        Feature_Score = Check_null(word, feature_score_dic)
        New_feature_dic[word] = Feature_Score
    Counts_Final_Features_Scores = Counter( New_feature_dic)
    Number_of_keywords = 10
    keywords =[]
    for word, fr in Counts_Final_Features_Scores.most_common(Number_of_keywords):
        keywords.append(word)
    
    return(keywords)
if __name__ == "__main__":    
    URL ="http://bbc.com"    
    Text, HTML =Web_Funtion(URL)
    Keywords  = Extract_keywords_Base(URL,Text, HTML,False)
    print (Keywords)


                                            


