import lxml
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


class Scrape:
    def __init__(self):
        self.url="https://tiny.cc/sck34y"
        self.reviews={}
        self.positive=[]
        self.negative=[]
        self.neutral=[]
    
    def get_reviews(self,s,url):
        s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        response = s.get(url,headers=s.headers)
        soup = BeautifulSoup(response.text,"lxml")
        return soup.find_all("span",{"data-hook":"review-body"})

    def get_tag(self,s,url):   #pagination to scrape 100 reviews
        s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        response = s.get(url,headers=s.headers)
        soup = BeautifulSoup(response.text,"lxml")
      
        try:
            link=soup.find("li",{"class":"a-last"})
            a=link.find('a')
            b="https://www.amazon.in"+a['href']
        
            return b
        except:
            pass 

    def sentiment(self,text):    # sentiment analysis

        score =TextBlob(text).sentiment.polarity
        if(score==0):
            self.neutral.append(text)
            return "neutral"
        elif(score>0):
            self.positive.append(text)
            return "positive"
        else:
            self.negative.append(text)
            return "negative" 

    def review_(self):   #Fectchimg the reviews
        link = 'https://www.amazon.in/OnePlus-Midnight-Black-128GB-Storage/product-reviews/B07DJHY82F/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        i=0
        with requests.Session() as s:
            while(i <=100):
                if(i>=100):
                    break
                try:
                    
                    for review in self.get_reviews(s,link):
                        
                        #self.reviews.append(review)    
                        print(i,")",f'{review.text}\n')
                        text=str(review.text)
                        self.reviews[str(i)]=text
                        t2=self.sentiment(text)
                        print("Analysis:",t2,"\n")
                            
                        i=i+1
                except UnicodeEncodeError:
                    pass     
                    
                link=self.get_tag(s,link)  

    def accuracy(self):
        pp=(len(s.positive)/len(s.reviews))*100
        np=(len(s.negative)/len(s.reviews))*100
        nep=(len(s.neutral)/len(s.reviews))*100


        print("There are",pp,"% positive reviews\n")
        print("There are",np,"% negative reviews\n")
        print("There are",nep,"% neutral reviews\n")


# database   
from pymongo import MongoClient 
client = MongoClient("mongodb://localhost:27017/") 
mydatabase = client['amazon'] 
mycollection=mydatabase['review']        

rec = mydatabase.review.insert(dict(s.reviews)) 
# print(rec)

s=Scrape()
s.review_()
print(s.positive)
s.accuracy()


