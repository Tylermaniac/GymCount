# import HTMLSession from requests_html
import requests
from bs4 import BeautifulSoup
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy


 
for l in range(0,100000):

	def create_browser(webdriver_path):
	    #create a selenium object that mimics the browser
		browser_options = Options()
	    #headless tag created an invisible browser
		browser_options.add_argument("--headless")
		browser_options.add_argument('--no-sandbox')
		browser = webdriver.Chrome(webdriver_path, chrome_options=browser_options)
		print("Done Creating Browser")
		return browser

	url = "http://connect2concepts.com/connect2/?type=circle&key=8E2C21D2-6F5D-45C1-AF9E-C23AEBFDA68B"
	browser = create_browser('/users/nemet/chromedriver.exe') #DON'T FORGET TO CHANGE THIS AS YOUR DIRECTORY
	browser.get(url)
	innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
	page_html = browser.page_source
	print(innerHTML)

# create an HTML Session object
#	print('Connecting to Webpage')
	# Use the object above to connect to needed webpage
#	resp = requests.get("http://connect2concepts.com/connect2/?type=circle&key=8E2C21D2-6F5D-45C1-AF9E-C23AEBFDA68B")
	 
#	print('Render JavaScript')
	# Run JavaScript code on webpage
#	resp.html.render()

	soup = BeautifulSoup(page_html, "lxml")
	 
	info = soup.find_all('div', attrs={'style': 'text-align:center;'})

	print('Finding 24 HTML locations')
	# Trying to put it in an array
	textContent = []
	for i in range(0, 23):
	    paragraphs = soup.find_all('div', attrs={'style': 'text-align:center;'})[i].text
	    textContent.append(paragraphs)
	# textContent = numpy.transpose(textContent)
	print('Acquiring Google credentials')
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open("Gym Count").sheet1

	print('Parsing strings')
	# StringParser Tyler Nemeth
	title = []
	total = textContent
	for j in range(0,23):
		for i in range(0,len(total[j])):
			if(total[j][i]=='('):
				break
			else:
				continue  # only executed if the inner loop did NOT break
			break 
		title.append(total[j][0:i])
	title = numpy.transpose(title)

	count = []
	for j in range(0,23):
		for i in range(0,len(total[j])):
			if(total[j][i]==':'):
				flag = 1
				if(flag == 1):
					break
				else:
					continue  # only executed if the inner loop did NOT break
				break
			else:
				continue  # only executed if the inner loop did NOT break
			break
		count.append(total[j][i+2:i+5])

	for i in range(0,23):
		if(count[i][1]=='U'):
			count[i] = count[i][:1]
		elif(count[i][2]=='U'):
			count[i] = count[i][:2]

	time = []
	for j in range(0,23):
		for i in range(0,len(total[j])):
			if(total[j][i]=='/'):
				break
			else:
				continue  # only executed if the inner loop did NOT break
			break 
		time.append(total[j][i-2:len(total[j])])

	#Concat for martin
	row4 = []
	for i in range(0,23):
		concat = title[i] + time[i]
		row4.append(concat)

	#Check for duplicates
	full = sheet.col_values(4)

	row5 = []

	#Print to google sheet
	for i in range(0, 23):
		values_list = sheet.col_values(1)
		row5.append('=if(counta(FILTER(D'+str(len(values_list)+1)+':D,D'+str(len(values_list)+1)+':D=D'+str(len(values_list)+1)+'))>1,1,0)')
		row = [title[i],int(count[i]),time[i],row4[i],row5[i]]
		print('Adding Row: ' + str(i))
		index = len(values_list)+1
		sheet.insert_row(row,index, value_input_option='USER_ENTERED')
	print('Sleeping for 30 min')
	sleep(1800)
