# import HTMLSession from requests_html
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
import numpy
 
# create an HTML Session object
session = HTMLSession()
 
# Use the object above to connect to needed webpage
resp = session.get("http://connect2concepts.com/connect2/?type=circle&key=8E2C21D2-6F5D-45C1-AF9E-C23AEBFDA68B")
 
# Run JavaScript code on webpage
resp.html.render()

soup = BeautifulSoup(resp.html.html, "lxml")
 
info = soup.find_all('div', attrs={'style': 'text-align:center;'})

# Trying to put it in an array
textContent = []
for i in range(0, 23):
    paragraphs = soup.find_all('div', attrs={'style': 'text-align:center;'})[i].text
    textContent.append(paragraphs)
# textContent = numpy.transpose(textContent)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Gym Count").sheet1

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
	
#Check for duplicates



#with open('counts.csv','a') as fd:
#    fd.write(myCsvRow)