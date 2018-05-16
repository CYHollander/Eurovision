from bs4 import BeautifulSoup
import inspect
import logging

logging.basicConfig(filename='errors.log',level=logging.DEBUG,filemode='w')

for year in range(1956,2019):
	filename = 'Eurovision%s.html' % str(year)
	with open(filename, 'r') as f:
		ev = BeautifulSoup(f.read(), 'html.parser')

	try:
		conductors = ev.find(id="Conductors").find_next("ul").find_all("li")
		conductors_table = ([c.get_text().strip().split(sep=' - ') for c in conductors])
	except Exception as e:
		fi = inspect.trace()[0]
		logging.debug(''.join([str(x) for x in [filename,'\n',e,'\n',fi.lineno,'\n',fi.code_context[0]]]))

	try:
		result_table=ev.find(id="Results").find_next("table").find_all("tr")
		headers=[th.contents[0] for th in result_table[0].find_all("th")]
		contents = [[td.get_text().strip().split(sep=',') for td in row.find_all("td")] for row in result_table[1:]]
	except Exception as e:
		fi = inspect.trace()[0]
		logging.debug(''.join([str(x) for x in [filename,'\n',e,'\n',fi.lineno,'\n',fi.code_context[0]]]))
	try:
		vote_table = ev.find(id="Scoreboard").find_next("table").find_all("tr")[2:]
		headers1= [row.find("td").get_text().strip() for row in vote_table]
		contents1 = [[int(td.get_text().strip()) if td.get_text()!= '' else 0 for td in row.find_all("td")[2:]] for row in vote_table]
	except Exception as e:
		fi = inspect.trace()[0]
		logging.debug(''.join([str(x) for x in [filename,'\n',e,'\n',fi.lineno,'\n',fi.code_context[0]]]))