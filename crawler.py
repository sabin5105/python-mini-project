import selenium
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings() # ignore SSL warning

URL = "https://www.gbif.org"

def main():
    # open gbig.txt
    temp = open("gbig.txt", "r", encoding="utf-8") # html copied file from url
    html = temp.read()
    temp.close()
    
    html = bs(html, "html.parser")
    
    # put src into the list from tag that include div > div > a class="imageGallery__img ng-scope isValid"
    img_list = html.select("div > div > a.imageGallery__img.ng-scope.isValid > img")
    img_src = []
    [img_src.append(img.attrs["src"].replace("/x260", "").replace("//", "https://")) for img in img_list] 
    
    #----dynamic crawling----
    # selenium, dynamic crawling
    # driver = webdriver.Chrome()
    # for i in tqdm(range(len(img_src))):
    #     driver.get(URL + img_src[i])
    #     time.sleep(2)
    #     print("here!")
    #     # img context_click() -> save image as -> save
    #     driver.find_element_by_tag_name("img").context_click()
    #     driver.find_element_by_id("context-menu-save-image-as").click()
    #     driver.find_element_by_id("file_name").send_keys(str(i))
    #     driver.find_element_by_id("save_image").click()
    #     time.sleep(2)
    # driver.close()
    
        
    #----static crawling----
    # print(img_src)
    # download image through url saved in img_src
    for i in tqdm(range(len(img_src))):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        img = session.get(img_src[i], verify=False)        
        
        with open("./images/" + str(i) + ".jpg", "wb") as f:
            f.write(img.content)
        time.sleep(2)
        
    print("Done")
    
if __name__=="__main__":
    main()
    
    