import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://")        #cluster name
db = cluster["NYAA"]    #database name
collection = db["Anime"]    #collection name
num=1 # page counter 
num = input("Enter the page number: ") #input the page number
num = int(num)
url = f"https://nyaa.si/?f=0&c=1_4&q=&p={num}" #url of the page
r = requests.get(url)
AnimeCheck = [] #array of titles
urlView=[] #array of links

def changePagelink(url):        #function to change the page number
    print(url)
    url2 = url.replace(f"p={str(num)}", f"p={str(num+ 1)}")
    print(url2)
    return url2


def MagnetLink(url):                #function to get the magnet link
    AnimeDictTemp = {}
    for i in url: 
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        magnet_url = soup.findAll('div',attrs={'class': 'panel-footer clearfix'})
        for div in magnet_url:
            Magnet=div.find('a')['href']
            print(Magnet)
            links = soup.find('a', attrs={'href': lambda L: L and L.startswith('magnet')}).get('href')
        print(links)
        title=soup.find('title').text
        print(title)
        if title not in AnimeCheck:
            AnimeDictTemp = {"title": title, "url": links , "Download": f"https://nyaa.si{Magnet}"}
            AnimeCheck.append(title)
            if collection.insert_one(AnimeDictTemp):
                     print("done updating")
                     AnimeDictTemp.clear()
        else:
            print("Already in the database") 
            continue
        
      

def ViewNyaaLinks(url):                             #function to get the links of the anime
   
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    urlView1=[]
    for i, tr in enumerate(trs):
        td_colspan2 = tr.find('td', {'colspan': '2'})
        a_tag = td_colspan2.find('a')
        href = a_tag['href']
        urlView1.append(f"https://nyaa.si{href}")
        print(urlView1[i])
    return urlView1

    
while r.request!=404:                        #loop to get all the pages
    urlView=ViewNyaaLinks(url)
    print("**************")
    MagnetLink(urlView)
    print("**************")
    url=changePagelink(url)
    print("**************")
    num+=1
    postcount = collection.count_documents({})
    print(postcount)
    print("**************")
    



