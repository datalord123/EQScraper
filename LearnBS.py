from bs4 import BeautifulSoup

html_doc = '''
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
'''

soup= BeautifulSoup(html_doc)
#Prettify turns an html document into a string adding strategic newlines and spacing in the process
#print (soup.prettify())

tag=soup.text
print type(tag)
print tag

'''
#Print title tag line
print soup.title

#Prints the tag of the title
print soup.title.name

#Print the string of the title
print soup.title.string

#print the name of parent tag of the title tag
print soup.title.parent.name

#Print the p tag line
print soup.p

#Print the name of class for the p tag
print soup.p['class']

#Find the first a tag line
print soup.a

#Find all lines with a tag
print soup.find_all('a')

#Find the line with id=3
print soup.find(id='link3')

#One common task is extracting all the URLs found within a page's <a> tags:
for link in soup.find_all('a'):
	print(link.get('href'))

# Another common task is extracting all the text from a page:
print(soup.get_text())	
'''





