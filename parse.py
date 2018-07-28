import requests
from bs4 import BeautifulSoup

url_to_scrape = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/schoolsdetails/8478'
r = requests.get(url_to_scrape)

# We now have the source of the page, let's ask BeaultifulSoup
# to parse it for us.
soup = BeautifulSoup(r.text, "html.parser")

# Down below we'll add our inmates to this list
table_list = []

# BeautifulSoup provides nice ways to access the data in the parsed
# page. Here, we'll use the select method and pass it a CSS style
# selector to grab all the rows in the table (the rows contain the 
# inmate names and ages).

for table in soup.select("table"):
	# Each tr (table row) has three td HTML elements (most people 
	# call these table cels) in it (first name, last name, and age)
	for loop_counter,t_row in enumerate(table.select('tr')):		
		cells = t_row.findAll('td')
		# Our table has one exception -- a row without any cells.
		# Let's handle that special case here by making sure we
		# have more than zero cells before processing the cells
		if len(cells) > 0:
			if loop_counter == 0: print ('HEADING:', cells[0])
			row = []
			for cell in cells: row.append(cell.text.strip())
			
			table_list.append(row)

			# Let's print our table out.
			print (row)
	print('='*10)