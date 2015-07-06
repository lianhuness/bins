#!/usr/bin/python
# -*- coding: utf-8 -*-
#test


import urllib, urllib2, cookielib
from urlparse import urljoin
from urlparse import urlparse
import pdb
from bs4 import BeautifulSoup as BS
from requests import session
import requests
import os

DIR = "bttang"
if not os.path.exists(DIR):
			os.makedirs(DIR)

MAIN_URL = "http://www.bttiantang.com"

s = session()
home = s.get(MAIN_URL)
b = BS(home.text)

hotlist = b.find(id='hotlst')
lists = hotlist.find_all('a')
lists = lists[1::2]

#lists = [urljoin(MAIN_URL, x.attrs['href']) for x in hotlist.find_all('a')]


cnt = 0
for link in lists:
	cnt+= 1
	print("\n\n\n============ %s out of %s \n\n" % (cnt, len(lists)))
	url = urljoin(MAIN_URL, link.attrs['href'])
	title = link.text.replace('/', '_')
	print(title)
	
	filename = DIR+"/"+title+".torrent"
	if os.path.exists(filename):
		print("******** %s exist, skip ** " % filename )
		continue

	res = s.get(url)
	html = BS(res.text, from_encoding="utf-8")

	divs = html.find_all('div', {'class':'tinfo'})
	lns = [div.find('a') for div in divs]
	
	if len(lns) == 0:
		continue

	highlns = [ln for ln in lns if ln.text.find('1080') > 0]

	downloadLink = ""
	if len(highlns) > 0:
		downloadLink = highlns[0]
	else:
		downloadLink = lns[0]

	fullURL = urljoin(MAIN_URL, downloadLink.attrs['href'])

	print(fullURL)

	parser = urlparse(fullURL)
	query = parser.query.split('&')

	data={'action': 'download',
		'id':21111,
		'uhash': "e6318208051c9e19ef7b89bf"
	}

	for info in query:
		node = info.split('=')
		if node[0] == 'id':
			data['id'] = node[1]
		if node[0] == 'uhash':
			data['uhash'] = node[1]

	req = requests.post("http://www.bttiantang.com/download2.php", data)

	with open(filename, 'wb') as file:
		file.write(req.content)




	




