import requests
from bs4 import BeautifulSoup
import pandas as pd

#get live data
def _GetDataFromWeb(url, liveData = True):

	if liveData:
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

		response = requests.get(url, headers=headers)
		data = response.text
	else:
		with open("file.txt", 'r') as f:
			data = f.read()
	return data


def _ParseData(data):
	parsedData = BeautifulSoup(data, 'html.parser')
	tables = parsedData.findAll("table")
	
	theTable = None
	
	for table in tables:
		if '/s/' in table.text and 'Director' in table.text:
			theTable = table
			break
			
	if theTable is None:
		theTable = tables[-1]
	

	rows = theTable.findAll('tr')

	validstrings = []

	for row in rows:
		text = row.text
		#print(text)
		if text and text.strip():
			t = text.replace(u'\u200b\u200b\u200b\u200b', u'').replace(u'\u200b', u'%').replace(u'/s/', u'')	
			validstrings.append([x.split('%') for x in t.strip().split("\xa0\xa0\xa0\xa0")])
			#validstrings.append(t)
					
	validstrings = [x[:2] for x in validstrings if x[0][0]!='']
	
	finedata = []
	
	for i in validstrings:
		if len(i)>1:
			finedata.append([i[0][0],i[1][0]])
		else:
			finedata.append(i[0][:2])
	
	
	names = [x[0] for x in finedata[1:]]
	titles = [x[1] for x in finedata[1:]]
	df = pd.DataFrame(names, columns=['Name'])
	df['Title'] = titles
	return df


def _geturlandsavetofile(url):
	data = _GetDataFromWeb(url)
	with open("file.txt", 'w') as f:
		f.write(data)
	

def Run(url, liveData=True):
	return _ParseData(_GetDataFromWeb(url, liveData))



		
if __name__ == '__main__':
	#_geturlandsavetofile("https://www.sec.gov/Archives/edgar/data/2186/0001654954-20-002248.txt")
	print(Run("", False))




