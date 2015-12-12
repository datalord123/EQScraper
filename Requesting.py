from bs4 import BeautifulSoup
import requests
s=requests.Session()
r=s.get('http://www.transtats.bts.gov/Data_Elements.aspx?Data=2')
soup=BeautifulSoup(r.text)

viewstate_element=soup.find(id='__VIEWSTATE')
viewstate=viewstate_element['value']

eventvalidation_element=soup.find(id='__EVENTVALIDATION')
eventvalidation = eventvalidation_element['value']
			   
r=s.post('http://www.transtats.bts.gov/Data_Elements.aspx?Data=2',
				data={
				 'AirportList' : 'BOS',
				 'CarrierList' : 'VX',
				 'Submit':'Submit',
				 '__EVENTTARGET':'',
				 '__EVENTARGUMENT':'',
				 '__EVENTVALIDATION':eventvalidation,
				 '__VIEWSTATE': viewstate})

f = open('virgin_and_logan_airport.html','w')
f.write(r.text)

'''	    
def get_options(soup,id):
	option_values=[]
	for option in soup.find(id=id):
		option.find('value')
		value=option.string
		option_values.append(value)
	return option_values	

def print_list(label,codes):
#	print '\n%s:' % label
	for c in codes:
		print c

def extract_data(page):
	data={'eventvalidation':'',
		  'viewstate':''}
	with open(page,'r') as html:
		soup = BeautifulSoup(html)

	return data	   



data=extract_data(r.text)
codes = get_options(soup,'CarrierList')
print_list('Carriers',codes)
codes = get_options(soup,'AirportList')
print_list('Carriers',codes)	
'''