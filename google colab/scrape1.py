# THis program will extract data from a dummy website for learning web scraping and thi sdatyaset willl have Book name,Price,rating,Author name(In future)
# Lets see how this work.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
Book_Name=[]
Author=[]
Price=[]
Availablity=[]
final=""
count=1000
for page in range(1,51):
  url = f"https://books.toscrape.com/catalogue/page-{page}.html"
  webpage = requests.get(url).text
  soup=BeautifulSoup(webpage,"lxml")
  for bookdiv in soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
    try:
      Book_Name.append(bookdiv.find("h3").a["title"])
    except:
      Book_Name.append(np.nan)
    final=str(bookdiv.find("h3").a["title"]).replace(" ","-").lower()
    #----------------------------------------------------------------------
    # This is to Initialise the stock available of the book
    url2=f"https://books.toscrape.com/catalogue/{final}_{count}/index.html"
    auth=requests.get(url2).text
    soup2=BeautifulSoup(auth,"lxml")
    #----------------------------------------------------------------------
    try:
      Author.append(soup2.find("div",class_="col-sm-6 product_main").h3.text)
    except:
      Author.append(np.nan)
    try:
      Price.append(bookdiv.find("p",class_="price_color").text)
    except:
      Price.append(np.nan)
    stock=""
    try:
      for i in soup2.find_all("td")[5].string.split()[2]:
        try:
          int(i)
          stock+=i
        except:
          pass
    except:
      stock=np.nan
    try:
      Availablity.append(int(stock))
    except:
      Availablity.append(np.nan)
    count-=1
datafr=pd.DataFrame({"Book Name":Book_Name,"Price":Price,"Availablity":Availablity})
print(datafr)
datafr.to_csv("books.csv",index=False)