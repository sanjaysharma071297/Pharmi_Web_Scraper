# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:37:24 2021

@author: Lenovo
"""



import pyodbc
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import json
import re

##############################################################################################################################
def link_Result(domain,link):
    page1 = requests.get(domain+link)
    return bs(page1.text, "lxml", from_encoding="utf-8")

def extarct_news(domain,link):
    soup2 = link_Result(domain,link)
    
    try:
        heading =soup2.find('div',class_='col pl-md-5 card-header').text.strip().replace('\n','').replace('\r','')
    except:
        heading=''
    try:
        summary =soup2.find('div',class_='col card-text').text.replace('\n','').replace('\r','').strip()
    except:summary=''
    
    Information=soup2.find('ul',class_='no-bullets small text-right')
    
    try:
        
        posted_company=Information.findAll('li')[0].text.replace('Author Company: ','')
    except:  
        posted_company=''
                
    try:
        website=Information.findAll('li')[3].text.replace('Author Website: ','')
    except:
        website=''
        
    try:
        posteddate=soup2.find('small',class_='font-italic').text.strip().replace('\n','').replace('\r','').split()[-1]
        
        
    except:posteddate=''   
     
    data =[heading,summary,posted_company,website,link,posteddate]
    return data

#################################################################################################################




search_term ='physical security'
search_qry=search_term.replace(' ','+')

domain = 'https://www.pharmiweb.com'

MainUrl ='https://www.pharmiweb.com/search/?query='+str(search_qry)+'&type=1'
page=requests.get(MainUrl)
soup=bs(page.text,'html.parser')
    
#PageCount
page=soup.findAll('li',class_='page-item')
#page_count = int(len(page))
page_count =int(1)
#AllPages
news=[]
count = 0
try:
    for i in range(1,page_count+1):
        url = MainUrl+'&page='+str(i)
        r = requests.get(url)
        soup1=bs(r.text,'html.parser')
        
        links = [a['href'] for a in soup1.find('tbody').find_all('a')]
        if(len(links) == 0):
           break
        for link in links:
            print(count);count+=1
            
        #finding links for news
            jobdata=extarct_news(domain,link)
            
            news_article = {
                'Keyword':search_qry,
                'Title':jobdata[0].replace("'",''),
                'Description': jobdata[1],
                'SourceCompany':jobdata[2],
                'Url':domain+jobdata[4],
                'website':jobdata[3],
                'PostedDate':jobdata[5]
                }
            news.append(news_article)
except Exception as e:
    print(e)

time_stamp=time.strftime("%d_%m_%Y")   # get today date
# create json file and add jobs in the file
with open('./Json/'+search_qry.replace('+','_')+time_stamp+'.json', 'w') as outfile:
    json.dump(news, outfile)
    print("successfull")                      

      

            
            
        
    
        
        
        
        
        
        
        
        
        
        
        
                