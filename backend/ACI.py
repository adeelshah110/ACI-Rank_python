#change
import sys
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib64/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/lib64/python3.6/site-packages')
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/lib/python3.4/site-packages/')
sys.path.append('/home/tko/himat/web-docs/lib/python3.6/site-packages/')
sys.path.append('/home/tko/himat/lib/python3.4/site-packages/')
#NEW LOCATION FOR PACKAGES ON SERVER
sys.path.append('/home/tko/himat/web-docs/keywordextraction/lib/python3.6/site-packages')
sys.path.append('/usr/lib/python3.4/site-packages')
sys.path.insert(0, '/home/tko/himat/web-docs/keywordextraction')
#sys.path.append('/home/tko/himat/packages/')
from collections import defaultdict 
import re 
import wikipedia
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
import lxml
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

from collections import defaultdict
sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')

sys.path.append('/home/tko/himat/web-docs/keywordextraction/pylibs/lib/python3.4/site-packages/')
stp ="january use jun jan feb mar apr may jul agust dec oct nov sep dec  product continue one two three four five please thanks find helpful week job experience women girl apology read show eve  knowledge benefit appointment street way staff salon discount gift cost thing world close party love letters rewards offers special close  page week dollars voucher gifts vouchers welcome therefore march nights need name pleasure show sisters thank menu today always time needs welcome march february april may june jully aguast september october november december day year month minute second secodns".split(" ")
common_nouns='debt est dec big than who '.split(" ")

spchars = re.compile('\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\+|\=|\\|\||\{|\[|\]|\}|\:|\;|\'|\"|\<|\,|\>|\?|\/|\.|\-')

import warnings
warnings.filterwarnings("ignore")
#1##########################################################################################11111111
###############################################################################################################################

#Section-01     stop words                  1.Stop_Words_list(name_of_file)

#Section-02     Scrapper,Web                1.Scrapper1(element)  2.scrapper2   3.scrapper3     4.scrapper_title           5.Web(urls)

#Section-03     NLP and Counters,POS        1.POS_seperator       2.Counters    3.Calc_word_frequency(nouns)

#Section-04     Divide URL parts            1.Divide_Url(url)     2.Url(url)

#Section-05     Features DOM                1.explode             2.get_text    3.Extract_headerAnchorTitle(soup)

#Section-06     Writting,Reading txt,csv    1.write                2. Writing_csv               3.Read_Text

#Section-07     Score Features              1.Score_f              2.Score

#Section-08     Meta,Keywords,Title         1.Meta_keywords(url)    2.Meta_GT(HTML)

########################################################################################################
#Section-01 Stop words for germon,Finnish,English
########################################################################################################
def Stop_Words_list(name_of_file): 
    
    english_stopwords_file=set(stopwords.words("english"))
    if name_of_file =='finnish_stopwords_file':
        txt_file= open('stopword_list/Finnish_StopWords_list.txt','r',encoding="utf-8")
        read_txt_file =txt_file.readlines()
        return[x.replace('\n','').replace(' ','') for x in read_txt_file]
       
    elif name_of_file =='germon_stopwords_file':
        txt_file= open('Dataset-germon/stopwords-de.txt','r',encoding="utf-8")
        read_txt_file =txt_file.readlines()
        return[x.replace('\n','').replace(' ','') for x in read_txt_file]       
    else:        
        return (english_stopwords_file)
    return(stop_word_list)
#1##########################################################################################11111111
#Section-2 Scrapper download the webpage and beautiful soup
###################################################################################################
def Scrapper1(element):
    if element.parent.name in ['html','style', 'script', 'head',  '[document]','img']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def Scrapper2(body):                #text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')      
    texts = soup.findAll(text=True)   
    name =soup.findAll(name=True) 
    visible_texts = filter(Scrapper1,texts)        
    return u" ".join(t.strip() for t in visible_texts)
#raw =Scrapper2(html)#text
def Scrapper3(text):                  #filters(text):  
    lines = (line.strip() for line in text.splitlines())    # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))# break multi-headlines into a line each
    return u'\n'.join(chunk for chunk in chunks if chunk)# drop blank lines


def Scrapper_title_4(urls):
  req = urllib.request.Request(urls, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()
  title=[]
  
  soup = BeautifulSoup(html, 'lxml') 
  title.append(soup.title.string)
  return(title,urls)

def Web(urls):
  req = urllib.request.Request(urls, headers={'User-Agent' : "Magic Browser"})
  con = urllib.request.urlopen(req)
  html= con.read()  

  soup = BeautifulSoup(html, 'lxml') 
  #keywordregex = re.compile('<meta\sname= ["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')  
  raw =Scrapper2(html)
  clean_text=Scrapper3(raw) 
  return(clean_text,soup)  

#####################################################################################################################
#Section-03 NLP and Counters
#####################################################################################################################
def POS_seperator(Text):
  adj=[]
  verb=[]
  nouns=[]

  for line in Text:
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)

    
    for x,y in tagged:
      if y in ['NNP','NNPS','NNS','NN']:
        nouns.append(x)
      if y in ['JJ', 'JJR', 'JJS']:
        adj.append(x)
      if y in ['VB','VBD','VBG','VBN','VBP']:
        verb.append(x)
  return (nouns,adj,verb)

def Count_fr(words):
  token=[]
  count=[]
  fr = Counter(words)
  for t,c in fr.most_common():
    token.append(t)
    count.append(c)
  return(token,fr,count)     
def Calc_word_frequency(nouns):
    
    top_words ={}  
    word=[]
    result =[]
    fr = Counter(nouns)    
    for x,c in fr.most_common():
        word.append([x,c])
        top_words[x]=c
    return(top_words)
###################################################################################################################
#Section-04  URL Division
######################################################################################################################
def Divide_Url(url):
    from urllib.parse import urlparse 
    host=[]
    obj=urlparse(url)    
    name =(obj.hostname)
    for x in name.split('.'):
        if x.lower() not in ['','https','www','com','-','php','pk','fi','http:','http']:
            host.append(x)
    return(host)
def Urls(url):
    path=[]
    host =Divide_Url(url)   
    for x in url.split('/'):
        for i in x.split('.'):
            for d in i.split('-'):
                if d.lower() not in ['','https','www','com','-','php','pk','fi','https:','http','http:','html','htm'] and d.lower() not in host:              

                    path.append(d.lower())
    return(host,path)

##############################################################################################################################################################
#Section-   Beautiful Soup find tags features
###############################################################################################################################################
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
        h_text =(h_text.lower())
        text.append(h_text)
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
    a_d ={}
    title_d={}
    h1_d['h1']= get_text(soup,'h1')
    h2_d['h2']= get_text(soup,'h2')
    h3_d['h3']=get_text(soup,'h3')
    h4_d['h4']= get_text(soup,'h4')
    h5_d['h5']= get_text(soup,'h5')
    h6_d['h6']= get_text(soup,'h6')
    
    a_d['a']= get_text(soup,'a') #alt tab or anchor
    title_d['title']= get_text(soup,'title')  #CALLing       
    H1=explode(h1_d)
    H2=explode(h2_d)
    H3=explode(h3_d)
    H4=explode(h4_d)
    H5=explode(h5_d)
    H6=explode(h6_d)    
    A=explode(a_d)    
    T= explode(title_d)
    
   
    return(H1,H2,H3,H4,H5,H6,A,T)
######################################################################################################################## 
#Section-6 Writing reading file in txt and csv
#######################################################################################################################

def Write(Text):
    words =' '
    for x in Text:
        text = '  '.join (x.split())
        words += text+' '
    return (words)
def Writing_csv(dic,file):
    import csv  
    f = open(file,'w',encoding='utf-8')
    writer = csv.writer(f)
    for k in dic.items():
        writer.writerow(k)

def Read_Txt(file):
    f=open(file,'r')
    read = f.readlines()
    f.close()
    gt =[]
    for x in read:
        URL= (x.split()[0])
        Gt =x.replace(URL,'')
               
        for y in Gt.split():
            y =y.strip("\n")
            y=y.strip(",")
            if y==" " or y is None:
                continue
            gt.append(y.lower())            
    return(URL,gt)  
######################################################################################################## 
#section-07 Score features
#Features_Score inputs candidate word,words of feature list and score,name of feature
#returns total score and features name 

#########################################################################################################
def Feature_Score(candidate_word,feature_words,score):
    total_score=0
    score_single_time =0
    

    for word_feature in feature_words:
        if word_feature ==candidate_word:
            total_score+=score
            score_single_time =score
                
    return(score_single_time) 
    


def Score_Features(word_fr,H1,H2,H3,H4,H5,H6,anchor,title,url_part1,url_parts,text_length):    
    word_score ={} 
            
    feature_names=defaultdict(list)
   
    #score = [score_h1,score_h2,score_h3,score_h4,score_h5,score_h6]
   

    for word,fr in word_fr.items(): 
        score_h1 = Feature_Score(word,H1,6)
        score_h2 = Feature_Score(word,H2,5)
        score_h3 = Feature_Score(word,H3,3)
        score_h4 = Feature_Score(word,H4,2)
        score_h5 = Feature_Score(word,H5,2)
        score_h6 = Feature_Score(word,H6,2)

        score_anchor = Feature_Score(word,anchor,1)
        score_title = Feature_Score(word,title,6)

        score_url_host = Feature_Score(word,url_part1,5)
        score_url_query = Feature_Score(word,url_parts,4)

        if text_length<50:
            tf_score =((fr/100)*50)
        else:
           tf_score=((fr/100)*20)    

        #f_score =s+s2+s3+s4+s5+s6+s7+s8+s9+s10+tf_score
        final_score_word = (score_h1+ score_h2+ score_h3+ score_h4+ score_h5+ score_h6+ score_anchor+ score_title+ score_url_host+ score_url_query+ tf_score)
        
        #Get the names of tags a word occurs work for display bbc['h1','h2']
        '''

        score_list = [score_h1,score_h2,score_h3,score_h4,score_h5,score_h6,score_anchor,score_title,score_url_host, score_url_query]        
        feature_name =['h1','h2','h3','h4','h5','h6','A','T','URL-H','URL-Q']
        for x in range(len(score_list)):
            if score_list[x]>0:                
                feature_names[word].append([feature_name[x],fr,final_score_word])
       '''

        

        word_score[word] = final_score_word
        #pr12[x]=final_pr
            
    return(word_score)

#k=Get_keywords(url)
########################################################################################
#Section- Meta Keywords ,Title
#############################################################################################

def Meta_keywords(url):   #returns groundtruth keywords of any webpage and bi gram keywords seperated by comma
    meta_keywords=[]
    multigrams_metat_keywords=[]
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html")
        title = soup.title.string
        meta = soup.find_all('meta')
        

        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keyword', 'keywords']:
                n= ('NAME    :',tag.attrs['name'].lower())
                k= (tag.attrs['content'])
                for x in k.split(","):
                    multigrams_metat_keywords.append(x.lower())
                    for i in x.split():
                        meta_keywords.append(i.lower())
    except:
        pass           
    return(meta_keywords,multigrams_metat_keywords)

def Meta_GT(html):
    keywordregex = re.compile('<meta\sname= ["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')

    keywordlist = keywordregex.findall(html)
    if len(keywordlist) > 0:
        keywordlist = keywordlist[0]
        keywordlist = keywordlist.split(", ")
    return (keywordlist)
#############################################################################################
#



######################################################################################################
def Feature_Score(candidate_word,feature_words,score):
    total_score=0
    score_single_time =0
    

    for word_feature in feature_words:
        
        if word_feature ==candidate_word:
            
            #total_score+=score
            score_single_time = score
                
    return(score_single_time)
           
def Tf_Score(fr,text_length):
    if text_length<50:
        tf_score =((fr/100)*50)
    else:
        tf_score=((fr/100)*20) 
    return (tf_score)

#x[0]=word_in wikipedia  x[1]= tf in wikipedia generated from csv file
          


def Remove_duplicates_GT(l):
    new_list =[]
    [new_list.append(x) for x in l if x not in new_list]
    return (new_list)

def Clean_CSV_Files(words):
    w=[]
    import string
    from string import digits
    exclude = set(string.punctuation)
    if type(words) is not list:
        words = [(spchars.sub(" ", i)).replace('\n','').strip().lstrip(digits)for i in words.split(',') if i not in exclude ]
    else:
        words =[(spchars.sub(" ", i)).replace('\n','').strip().lstrip(digits)for i in words if i not in exclude ]

    for x in words:
        if len(x)>0:
            w.append(x)
    return(w)



#####################################################################################
#language detection
###################################################################################
import sys
try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print ('[!] You need to install nltk (http://nltk.org/index.html)')
def _calculate_languages_ratios(text):  
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]    
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
       
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) 
    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):
    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    stop_words_for_language = set(stopwords.words(most_rated_language))

    return most_rated_language,stop_words_for_language