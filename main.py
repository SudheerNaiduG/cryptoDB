import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import sys
import traceback
client=pymongo.MongoClient("ENTER YOUR MONGODB URL TO UPDATE THE CRYPTO PRICES")
#print(client.list_database_names())
db=client.price
options = webdriver.ChromeOptions()
options.binary_location='/app/.apt/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

url = "https://wazirx.com/exchange/BTC-INR"
while True:
	print("Running")
	try:
		driver = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver',options=options)
		driver.get(url)
		time.sleep(5)
		html=driver.page_source
		driver.quit()
		soup = BeautifulSoup(html, "html.parser")
		all_divs = soup.find('div', {'class' : 'sc-iELTvK bZNgpE'})
		job_profiles = all_divs.find_all('a')	
		for i in job_profiles:
			market_name=i.find('span',{'class':'market-name-text'})
			temp=i.find('span',{'color':'#00C853','class':'sc-bwzfXH cFmqCk'})
			if temp is not None:
				market_change="+"+temp.text.encode('utf-8').decode('ascii', 'ignore')[1:]
			else:
				temp=i.find('span',{'color':'#f44336','class':'sc-bwzfXH jsJuLQ'})		

				market_change="-"+temp.text.encode('utf-8').decode('ascii', 'ignore').replace("-","")[1:]
			price=i.find('span',{'class':'price-text ticker-price'}).text.encode('utf-8').decode('ascii', 'ignore')
			market_name=market_name.text[:-4].upper()
			db.crypto.update_one({"market_name":market_name},{"$set":{"market_change":market_change,"price":price}},upsert=True)	
	except:
		print(traceback.format_exc())
