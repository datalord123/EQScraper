from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import requests
import re
import os
import __builtin__


url='http://www.kentuckyequestrian.com/main.cfm?action=greenpages'
filename='KentuckyEQData.csv'
baseurl='http://www.kentuckyequestrian.com/{}'

def extract_contact(url,Phone):
	list = list = __builtin__.list
	r=requests.get(url)
	soup=BeautifulSoup(r.content,'lxml')
	tbl=soup.findAll('table')[2]
	set=[]
	Street = []
	Zip = []
	State=[]
	l=['0','1','2','3','4','5','6','7','8','9']
	exc=['P.O.','PO','P.O']
	
	Content=tbl.findAll('p')
	if len(Content)>0: 
		Contact=Content[0] 
		Body=''
		
		for br in Contact.findAll('br'):
			next = br.nextSibling
			if not (next and isinstance(next,NavigableString)):
				continue
			next2 = next.nextSibling
			if next2 and isinstance(next2,Tag) and next2.name == 'br':	
				text = re.sub(r'[\n\r\t\xa0]','',next).replace('Phone:','').strip()
				set.append(text)
		s= [s for s in set if s != Phone]
		next=[]
		for i in s: 
			step= i.split(',')
			step=[w.strip() for w in step]
			next = next + step
		next = filter(None, next)
		for i in next:
			if i[0] in l or any(e in i for e in exc): 
				Street.append(i.strip())
			if len(i)>5 and i[-5] in l and i[-1] in l and i[0:4] not in exc and i[0] not in l:
				#print i
				step= i[-5:].strip()
				Zip.append(step)
				if i[-7] == ' ':
					State.append(i[-9:-7])
				else:
					State.append(i[-8:-6])
		set=[]
		ContactName = Contact.findAll('b')
		if len(ContactName)>1:
			ContactName=ContactName[1].string.strip()
		
		else:
			ContactName=''			
				
		Email = Contact.findAll(text=re.compile('@'))		
		if not Email:
			Email=''
		else:
			for i in Email:
				if '.com' in i:
					Email=i

		Website = Contact.findAll(text=re.compile('http'))
		if not Website:
			Website=''
		else:
			Website=Website[0]		
	else:
		set=['','','','','','','']		
	
	if len(Content)>1:
		Body=Content[1]#		
		Body = Body.text
		if not State:
			State=''
		else:
			State= State.pop(0)
		if not Zip:
			Zip=''
		else:	
			Zip=Zip.pop(0)
		if not Street:
			Street=''
		else:		
			Street=Street.pop(0)
		
		if isinstance(Email,list): 
			if not Email:
				Email=''
			else:	
				Email=Email.pop(0)		
		Street=re.sub(r'[\n\r\t\xa0]','',Street).encode('ascii','ignore').strip()		
		State = re.sub(r'[\n\r\t\xa0]','',State).encode('ascii','ignore').strip() 			
		Zip = re.sub(r'[\n\r\t\xa0]','',Zip).encode('ascii','ignore').strip()
		ContactName=re.sub(r'[\n\r\t\xa0]','',ContactName).encode('ascii','ignore').strip()		
		Email= re.sub(r'[\n\r\t\xa0]','',Email).encode('ascii','ignore').strip()							
		Website = re.sub(r'[\n\r\t\xa0]','',Website).encode('ascii','ignore').strip()
		Body = re.sub(r'[\n\r\t\xa0]','',Body).encode('ascii','ignore').strip()
		set.extend([Street,State,Zip,ContactName,Email,Website,Body])
	return set
			
def extract_data(soup,baseurl,Desc):
	data = []
	info = {}		
	tbl = soup.findAll('table')[2]
	for tr in tbl.findAll('tr')[3:]: #Tinker Records
		name, city, phone, url = tr.findAll('td')[:4]
		
		info['CategoryDesc']= Desc
		if name.string is not None:
			CompanyName=name.string.strip()
			CompanyName=re.sub(r'[\n\r\t\xa0]','',CompanyName).encode('ascii','ignore').strip()
		else:
			CompanyName=''
		if city.string is not None:
			City=city.string.strip()
			City=re.sub(r'[\n\r\t\xa0]','',City).encode('ascii','ignore').strip()
		else:
			City=''
		if phone.string is not None:
			Phone=phone.string.strip()
			Phone = re.sub(r'[\n\r\t\xa0]','',Phone).encode('ascii','ignore').strip()
			#Phone=phone.string.strip()
		else:
			Phone=''			
		info['CompanyName'] = CompanyName
		info['City']=City
		info['Phone']=Phone	
		url = baseurl.format(url.a['href'])
		print Desc,CompanyName
		set= extract_contact(url,Phone)
		#print list		
		info['Street']=set[0]
		info['State']=set[1]
		info['ZipCode']=set[2]
		info['ContactName']=set[3]
		info['Email']=set[4]
		info['Website']=set[5]
		info['CompanyDesc']=set[6]
		data.append(info.copy())
	return data 

def main(url,baseurl,filename):
	r=requests.get(url)
	soup=BeautifulSoup(r.content)
	List = soup.findAll('table')[2]
	data=[]
	for tr in List.find_all('tr')[0:]: #Tinker Categories
		url=baseurl.format(tr.a['href'])
		r=requests.get(url)
		soup=BeautifulSoup(r.content)
		Desc=tr.a.string.strip()		
		step= extract_data(soup,baseurl,Desc)
		data=data+step
		keys = data[0].keys()
	if os.path.exists(filename):
		os.remove(filename)	
		with open(filename,'wb') as f:
			dict_writer = csv.DictWriter(f,keys)
			dict_writer.writeheader()
			dict_writer.writerows(data)
	else:
		with open(filename,'wb') as f:
			dict_writer = csv.DictWriter(f,keys)
			dict_writer.writeheader()
			dict_writer.writerows(data)	

main(url,baseurl,filename)


