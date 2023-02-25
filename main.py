from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time
main_df = pd.read_csv('/output.csv')

try:
    chrome_driver = webdriver.Chrome('chromedriver.exe')
except:
    print("Update Your Chrome Driver")

input = ['rrr','#kgf'] #hashtag or keywords------------------------------------------------------INPUT
limit = 20 # limit of tweet for each (#hashtag or keywords)---------------------------------------INPUT
def find_particular_status_link(links, specific_string):
    for link in links:
        if specific_string in link.get('href'):
            return link.get('href')
    return None

def correct_input(inp):
    if '#' in inp:
        return inp 
    else :
        return '"' + inp + '"'

for k in input:
    chrome_driver.get('https://twitter.com/')
    WebDriverWait(chrome_driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')))

    artical1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[1]/div/div/div/article'
    search = chrome_driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')

    search.send_keys(correct_input(k) + ' lang:en')
    search.send_keys(Keys.ENTER)

    WebDriverWait(chrome_driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a')))
    chrome_driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a').click()

    WebDriverWait(chrome_driver,10).until(EC.presence_of_element_located((By.XPATH,artical1)))
    data = chrome_driver.find_elements(By.XPATH,'//*[@id="id__cmzkgf1trft"]/div[1]/div/a/div/div[1]/span/span')
    soup = BeautifulSoup(chrome_driver.page_source,'html5')
    data = soup.find_all('div',class_ = 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')

    ans = []
    while True:
        for t in data[1:]:
            if t :
                head = t.find('div',class_ = 'css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l')
                tweet = t.find('div',class_ = 'css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
                links = t.find_all('a')
                if head and tweet :
                    link = find_particular_status_link(links,'/status/')
                    if '@' in head.text:
                        temp = head.text.split('@')
                        if len(temp) == 2:
                            name,usename = head.text.split('@')
                        else:
                            continue
                    else:
                        continue
                    if '·' in usename:
                        usename,tdate = usename.split('·')
                        if 'Dec' in tdate:
                            break
                    else:
                        continue
                    tweet_text = tweet.text
                    main_link = 'https://twitter.com' + link 
                    if main_link not in [ans[x]['link'] for x in range(len(ans))]:
                        ans.append({
                            'name' : name,
                            'username' : '@' + usename,
                            'tweet' : tweet_text ,
                            'link': main_link
                        })
        chrome_driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        data = chrome_driver.find_elements(By.XPATH,'//*[@id="id__cmzkgf1trft"]/div[1]/div/a/div/div[1]/span/span')
        soup = BeautifulSoup(chrome_driver.page_source,'html5')
        data = soup.find_all('div',class_ = 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')
        if len(ans) > limit:
            break
    # print(ans)
    df = pd.DataFrame(ans)
    print(df)
    print('data store in output.csv file successfully')
    main_df = pd.concat([main_df,df],axis=0)
    main_df.to_csv('/output.csv')
