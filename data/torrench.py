#! /usr/bin/python3

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

import os
import sys
import argparse

def init(args):
	# Resolve arguments - BEGIN
	input_title = args.search
	page_limit = args.limit
	if args.clear_html:
		home = os.path.expanduser('~')
		temp_dir = home+"/.torrench/temp/"
		files = os.listdir(temp_dir);
		if files:
			count=1
			for i in files:
				os.remove(i);
				count = count+1;
			print("\nRemoved %d file(s).\n" %count)
		else:
			print("\nNothing to remove\n")
		sys.exit()
	if input_title == None:
		print("\nInput string expected.\nUse --help for more\n");
		sys.exit();
	elif page_limit <= 0 or page_limit > 50:
		print("Enter valid page input [0<p<=50]")
		sys.exit();
	else:
		main(input_title, page_limit);
	# Resolve input arguments - END

def main(input_title, page_limit):
	try:
		## Adding imports here since they are only required if this function is called.
		import requests
		from bs4 import BeautifulSoup
		from tabulate import tabulate
		from termcolor import colored
		import find_url
	except ImportError as e:
		print(e);
		print("Please install and retry.\n")
		sys.exit()
		
	# Get proxy list
	url_list = []
	url_list = find_url.find_url_list()
	
	title = input_title.replace(" ", "+")
	total_result_count = 0
	page_result_count = 9999
	details_link = {}
	details_name = {}
	masterlist = []
	
	try:
		# Traverse on basis of page_limit input
		for p in range(page_limit):
			# If results in a page are <30, break loop (no more remaining pages are fetched)
			if page_result_count < 30:
				break;
			
			if page_limit > 1:
				fetch_status_str = "\nFetching from page: "+str(p+1)
			else:
				fetch_status_str = "\n(Optional) Use [-p] option to specify pages.\n\nFetching results (Max: 30)...\n(Might take longer. Be patient)" 
			print(fetch_status_str);
			
			page_result_count = 0
			# Determine proxy site to use - list to proxy sites is obtained from find_url module
			url_list_count = 0
			url = url_list[url_list_count]
			search = {'q':title, 'category': '0', 'page': p, 'orderby':'99'}
			while(url_list_count < len(url_list)):
				try:
					raw = requests.get(url+"/s/", params=search)
					raw = raw.content
					break;
				except requests.exceptions.ConnectionError as e:
					print("Link Not reachable... Trying next proxy...");
					url_list_count += 1
					url = url_list[url_list_count]
			# End determining proxy site
			soup = BeautifulSoup(raw, "lxml")
			# Result found or not? 
			try:
				content = soup.find_all('table', id="searchResult")[0]
			except IndexError:
				if p == 0:
					print("\nNo results found for given input!");
					break	
					
			data = content.find_all('tr')
			mylist = []
			### Extraction begins here ###
			for i in data:
				name = i.find('a', class_="detLink")
				uploader = i.find('a', class_="detDesc")
				comments = i.find('img', {'src': '/static/img/icon_comment.gif'})
				if comments != None:
					comment = comments['alt'].split(" ")[-2] #Total number of comments
				else:
					comment = "0"
				if name == None or uploader == None:
					continue;
				name = name.string
				uploader = uploader.string 
				total_result_count+=1		
				page_result_count+=1
				categ = i.find('td', class_="vertTh").find_all('a')[0].string
				sub_categ = i.find('td', class_="vertTh").find_all('a')[1].string
				is_vip = i.find('img', {'title': "VIP"})
				is_trusted = i.find('img', {'title': 'Trusted'})
				if(is_vip != None):
					name = colored(name, "green")
					uploader = colored(uploader, 'green')
				elif(is_trusted != None):
					name = colored(name, 'magenta')
					uploader = colored(uploader, 'magenta')
				seeds = i.find_all('td', align="right")[0].string
				leeches = i.find_all('td', align="right")[1].string
				date = i.find('font', class_="detDesc").get_text().split(' ')[1].replace(',', "")
				size = i.find('font', class_="detDesc").get_text().split(' ')[3].replace(',', "")
				torr_id = i.find('a', {'class': 'detLink'})["href"].split('/')[2];
				link = url+"/torrent/"+torr_id		
				### Extraction ends here ###
				
				# Storing each row result in mylist
				mylist = [categ+" > "+sub_categ, name, "--"+str(total_result_count)+"--", uploader, size, seeds, leeches, date, comment]
				# Further, appending mylist to a masterlist. This masterlist stores the required result
				masterlist.append(mylist)
				
				# Dictationary to map torrent name with corresponding link (Used later)
				details_link[str(total_result_count)] = link
				details_name[str(total_result_count)] = name
			print(">> "+str(page_result_count)+" torrents");
	except KeyboardInterrupt:
		print("\nAborted!\n")
	
    # Print Results and fetch torrent details
	if(total_result_count > 0):
		print("\n\nS=Seeds; L=Leeches; C=Comments");
		final_output = tabulate(masterlist, headers=['TYPE', 'NAME', 'INDEX', 'UPLOADER', 'SIZE','S','L', 'UPLOADED', "C"], tablefmt="grid")
		print(final_output);
		print("\nTotal: "+str(total_result_count)+" torrents");
		exact_no_of_pages = total_result_count//30
		has_extra_page = total_result_count%30
		if has_extra_page > 0:
			exact_no_of_pages +=1			
		print("Total pages: "+str(exact_no_of_pages));
		print("\nFurther, a torrent's details can be fetched (Description, comments, download(Magnetic) Link, etc.)");
		
		# Fetch torrent details
		import details
		print("Enter torrent's index value to fetch details (Maximum one index)\n");
		option = 9999
		while(option != 0):
			try:
				option = int(input("(0 = exit)\nindex > "));
				if option > total_result_count or option < 0 or option == "":
					print("**Enter valid index**\n\n");
					continue;
				elif option == 0:
					break;
				else:
					selected_link = details_link[str(option)]
					selected_name = details_name[str(option)]
					print("Fetching details for torrent index [%d] : %s" %(option, selected_name));
					file_url = details.get_details(selected_link, str(option))
					print("\nFile URL: "+file_url+"\n\n"); 
			except KeyboardInterrupt:
				break;
			except ValueError:
				print("Check input! (Enter one (integer) index at a time)\n\n");
		print("\nBye");

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A simple torrent search tool.")
	parser.add_argument("search", help="Enter search string", nargs="?", default=None)
	parser.add_argument("-p", "--page-limit", type=int, help="Number of pages to fetch results from (1 page = 30 results).\n [default: 1]", default=1, dest="limit")
	parser.add_argument("-c", "--clear-html", action="store_true", default=False, help="Clear all torrent description HTML files and exit.")
	parser.add_argument("-v", "--version", action='version', version='%(prog)s v1.0', help="Display version and exit.")
	args = parser.parse_args()
	init(args);
