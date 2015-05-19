from bs4 import BeautifulSoup
import csv

soap = BeautifulSoup(open('victimstable.html' ,'r'))

cheatsheet = open("cheatsheet.csv", "w")
open_file_object = csv.writer(cheatsheet)

open_file_object.writerow(["Name","Survived"])

for tr in soap.find_all('tr'):
	for i, td in enumerate(tr.find_all('td')):
		if i== 0:
			familyName = td.find_all('span', itemprop='familyName')[0].contents
			familyName = familyName[0].strip() if familyName else ''
			familyName = familyName[:1].upper() + familyName[1:].lower()
			givenName = td.find_all('span', itemprop='givenName')[0].contents
			givenName = givenName[0].strip() if givenName else ''
			honorificPrefix = td.find_all('span', itemprop='honorificPrefix')[0].contents
			honorificPrefix = honorificPrefix[0].strip() if honorificPrefix else ''


			open_file_object.writerow([u'{}, {}. {}'.format(familyName,  honorificPrefix, givenName), 0])

soap = BeautifulSoup(open('survivorstable.html' ,'r'))


for tr in soap.find_all('tr'):
	for i, td in enumerate(tr.find_all('td')):
		if i== 0:
			familyName = td.find_all('span', itemprop='familyName')[0].contents
			familyName = familyName[0].strip() if familyName else ''
			familyName = familyName[:1].upper() + familyName[1:].lower()
			givenName = td.find_all('span', itemprop='givenName')[0].contents
			givenName = givenName[0].strip() if givenName else ''
			honorificPrefix = td.find_all('span', itemprop='honorificPrefix')[0].contents
			honorificPrefix = honorificPrefix[0].strip() if honorificPrefix else ''


			open_file_object.writerow([u'{}, {}. {}'.format(familyName,  honorificPrefix, givenName), 1])



cheatsheet.close()
