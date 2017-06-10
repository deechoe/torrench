'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

This file is part of Torrench.

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>. 
'''

from bs4 import BeautifulSoup
import urllib2
import os;

def get_details(url, index):
	home = os.path.expanduser('~')
	main_dir = home+"/.torrench/"
	temp_dir = main_dir+"temp/"
	icon_dir = main_dir+"icons/"
	vip_icon = icon_dir+"vip.gif"
	trusted_icon = icon_dir+"trusted.png"
	uploader_icon = ["<img src='"+vip_icon+"'>", "<img src='"+trusted_icon+"'>"]
	
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url, headers=hdr)
	raw = urllib2.urlopen(req).read()

	unique_id = url.split('/')[-1]
	file_name = unique_id+".html"
	
	soup = BeautifulSoup(raw, "lxml")
	content = soup.find('div', id="details")
	nfo = content.find_all('div', class_="nfo")[0].encode('utf-8')
	dt = content.find_all('dt')
	dd = content.find_all('dd')

	title = "(Index: "+index+") - "+soup.find('div', id="title").string.encode('utf-8')
	name = soup.find('div', id="title").string.encode('utf-8')
	magnet = soup.find('div', class_="download").a["href"]
	comment = soup.find_all('div', class_='comment')
	commenter = soup.find(id="comments").find_all('p')
	
	# Check Uploader-Status
	
	style_tag = "<style> pre {white-space: pre-wrap; text-align: left} h2, .center {text-align: center;} .vip {color: #336600} .trusted {color: #FF00CC}  body {margin:0 auto; width:70%;} table, td, th {border: 1px solid black;} td, th {text-align: center; vertical-align: middle; font-size: 15px; padding: 6px} .boxed{border: 1px solid black; padding: 3px} </style> "
	begin_tags = "<!DOCTYPE html><html><head><meta http-equiv='Content-type' content='text/html;charset=utf-8'> <title>"+title+"</title>"+style_tag+"</head><body>"
	end_tags = "</body></html>"

	# File opens here
	if not os.path.exists(temp_dir):
		os.makedirs(temp_dir)	
	f = open(temp_dir+unique_id+".html", "w")
	f.write(begin_tags)
	f.write("<h2><u><a href="+url+" target='_blank'>"+name+"</a></u></h2><br />")
	f.write("<table align='center'>")

	# The info table
	for i in dt:
		dt_str = i.get_text().encode('utf-8').replace(":", "")
		f.write("<th>"+dt_str+"</th>")
	f.write("</tr>\n<tr>\n")
	for j in dd:
		dd_str = j.get_text().encode('utf-8').replace(":", "")
		if j.img != None:
			if j.img['title'] == 'VIP':
				dd_str = "<div class='vip'>"+dd_str+"</div>" + uploader_icon[0];
			elif j.img['title'] == 'Trusted':
				dd_str = "<div class='trusted'>"+dd_str+"</div>" + uploader_icon[1];
				
		f.write("<td>"+dd_str+"</td>")

	f.write("</tr></table><br />")
	# Magnetic link
	f.write("<div class='center'><a href="+magnet+" target='_blank'>[Magnetic Link (Download)]</a></div><br />")

	# Printing Description
	f.write("<div class='boxed'>")
	f.write("<h2><u> DESCRIPTION </u></h2>")
	f.write("<pre>")
	f.write(nfo)
	f.write("</pre></div>")
	f.write("<div class='boxed'>")
	f.write("<h2><u> COMMENTS </u></h2>")
	f.write("<pre class='center'>(All comments might not be fetched. It's Because probably thats how its on website itself. Not to blame the tool)\n</pre>")
	#End Description

	#Printing Comments
	if commenter != []:
		f.write("<table align='center'>")
		for i, j in zip(commenter, comment):
			f.write("<tr><th>"+i.get_text().encode("utf-8")+"</th>")
			f.write("<td><pre>"+j.get_text().encode("utf-8")+"</pre></td></tr>")
		f.write("</table><br />");
	else:
		f.write("<div class='center'><pre>No comments fetched!</pre></div>") 
	f.write("</div><br />");
	# End Comments

	f.write("<div class='center'><a href="+magnet+" target='_blank'>[Magnetic Link (Download)]</a></div><br /><br />")
	f.write(end_tags);
	f.close();
	
	file_url = "file://"+temp_dir+file_name
	return file_url
	
if __name__ == "__main__":
	print "It's a module. Can only be imported!"
	
