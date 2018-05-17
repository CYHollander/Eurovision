from bs4 import BeautifulSoup
import re
import inspect
import logging
import numpy as np
import pandas as pd

df=[]

logging.basicConfig(filename='errors.log',level=logging.DEBUG,filemode='w')

for year in range(1956,2019):
	ydf=pd.DataFrame(columns=['Year','Country'])
	filename = 'Eurovision%d.html' % year
	with open(filename, 'r') as f:
		ev = BeautifulSoup(f.read(), 'html.parser')
        
	for invisible_data in ev.find_all(style="display:none"): invisible_data.decompose()

	if year <1999:
		try:
			conductors = ev.find(id="Conductors").find_next("ul").find_all("li")
			conductors_table = ([[year]+re.split(r'\W+[-–]\W+',c.get_text().strip()) for c in conductors])
			ydf=pd.merge(ydf,pd.DataFrame(conductors_table,columns=['Year','Country','Conductor']),how="right")
			
		except Exception as e:
			fi = inspect.trace()[0]
			logging.debug(''.join([str(x) for x in [filename,'\n',e,'\n',fi.lineno,'\n',fi.code_context[0]]]))

	try:
		results_id = "Results" if year < 2004 else "Final"
		result_table=ev.find(id=results_id).find_next("table").find_all("tr")
		headers=['Year']+[th.contents[0] for th in result_table[0].find_all("th")]
		results = [[year]+[td.get_text().strip() for td in row.find_all("td")] for row in result_table[1:]]
		ydf=pd.merge(ydf,pd.DataFrame(results, columns=headers),how="outer")
		num_countries= len(results)
	except Exception as e:
		fi = inspect.trace()[0]
		logging.debug(''.join([str(x) for x in [filename,'\n',e,'\n',fi.lineno,'\n',fi.code_context[0]]]))

	if year > 1956:
		try:
			vote_table_id = "Voting_structure" if year == 1981 else re.compile("Scoreboard|Score_sheet")\
			 if year < 2004 else "Final_2"
			vote_table = ev.find(id=vote_table_id).find_next("table")
			if year > 2008:
				vote_table=vote_table.find_next("table")
			vote_rows=vote_table.find_all("tr")[1:1+num_countries+1]
			first_headers = ['Country'] + (['Jury Score'] if year >= 2016 else [])
			vote_headers = first_headers+[re.search("File:ESC(.*).svg",tag['href']).group(1) for tag in vote_rows[0].find_all("a")]
			offset = 0 #if year < 2016 else 1
			votes = [[td.get_text().strip() if td.get_text()!= '' else '0' for td in\
			 row.find_all("td")[offset:]] for row in vote_rows[1:]]
			ydf=pd.merge(ydf,pd.DataFrame(votes, columns=vote_headers))
		except Exception as e:
			print(e)
    
	df=df+[ydf]

df=pd.concat(df)
with open ("eurovision_data.csv", 'w', newline='') as evdata:
	df.to_csv(evdata)