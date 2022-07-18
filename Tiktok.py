import requests
#import utilities
import pandas as pd
from bs4 import BeautifulSoup as BS 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#/workspace/Discord_Bot_SNSPost/chromedriver
class TikTokAPI:
    def __init__(self,API_KEY,APPID,CLIENTSECRET,CHANNEL_NAME):
        self.appid=APPID
        self.secret=CLIENTSECRET
        self.key=API_KEY
        self.channel_name=CHANNEL_NAME
        self.maxResult=1
        self.url="https://www.tiktok.com"
        self.driver=None
        self.driverpath="D:\Python_Scripts\Selenium\chromedriver_103_win32\chromedriver.exe"

    def create_driver(self,driverpath,brave="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"):
        options = Options()
        options.binary_location = brave
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(chrome_options=options,executable_path=driverpath)

    def get_videos(self,page_souce):
        soup = BS(page_souce, 'html.parser')
        videos=soup.find_all("div",{"class":"tiktok-x6y88p-DivItemContainerV2"})
        return videos
    def get_video_info(self,video_div):
            href=video_div.find("a").get("href")
            likes=video_div.find("strong",{"class":"video-count"}).text
            title=video_div.find("a",{"class":"tiktok-1wrhn5c-AMetaCaptionLine"}).get("title")
            return title,likes,href
    def get_account_df(self,channel_name):
        if not self.driver:
            self.create_driver(self.driverpath)

        self.driver.get(self.url+"/@"+channel_name.replace("@",""))
    
        page = self.driver.page_source
        self.driver.quit()
        self.driver=None
        videos=self.get_videos(page)
        print(len(videos))
        video_data=[]
        post_n=len(videos) 
        post_r=0
        for video in videos:
            if video:
                title,likes,href=self.get_account_df(video)
                print(title,likes,href)
                video_data.append({"title":title,"likes":int(likes),"href":href,"post_n":post_n,"post_r":post_r})
                post_n-=1
                post_r+=1

        return pd.DataFrame(video_data)
        
    def get_latest_post(self,channel_name):
        if not self.driver:
            self.create_driver(self.driverpath)

        self.driver.get(self.url+"/@"+channel_name.replace("@",""))
        #page = requests.get(self.url+"/@"+channel_name.replace("@","")).text
        page = self.driver.page_source
        self.driver.quit()
        self.driver=None
        soup = BS(page, 'html.parser')
        videos=soup.find_all("div",{"class":"tiktok-x6y88p-DivItemContainerV2"})
        print(len(videos))
        href=videos[0].find("a").get("href")
        likes=videos[0].find("strong",{"class":"video-count"}).text
        title=videos[0].find("a",{"class":"tiktok-1wrhn5c-AMetaCaptionLine"}).get("title")
        return {"title":title,"likes":int(likes),"href":href}


def main():
    api=TikTokAPI("TEST","TEST","test","gomitai")
    #last_post=api.get_latest_post(api.channel_name)
    #print(last_post)
    df=api.get_account_df(api.channel_name)
    df.to_csv(api.channel_name+".csv",index=False)

if __name__=="__main__":
    main()