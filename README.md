# Torrench - Torrent search made simple
Torrench is a simple command-line tool that fetches torrents and displays results **within terminal window**. It does this by scrapping _thepiratebay (proxy) sites_. Once torrent results are fetched, torrench can further fetch torrent details as well. Details include torrent Description, comments, as well as download (magnetic) link. (Basically everything required to choose a torrent).

_Torrench initially began as a python learning project for me. I am sure there are ways to implement code I wrote in a better/efficient way. If you find any, please **update me**._

_I'll continue updating it, add new features and try making it better and more efficient._
_If you find this tool helpful, spread the word please. Thank you!_

## Features
* ~~ads ads ads~~ Now surf torrents **Ad-free**
* Simple to use.
* Display search results in tabular form.
* Get complete torrent details (Description, comments, torrent download). Torrent details are available in dynamically-generated HTML pages.
* Display colored results on basis of _uploader's_ status (Very useful when choosing torrent). (If you are familiar with _thepiratebay_, you must be knowing that it divides _uploaders_ into 3 categories)
  * VIP Uploader ![VIP Uploader](/icons/vip.gif)
  * Trusted Uploader ![Trusted Uploader](/icons/trusted.png)
  * General Uploader
* Fetch torrents on basis of pages [1 page yields 30 results (max)].
* More to come...


## Requirements and Installation
1. Requires [Python3](https://www.python.org/downloads/)
2. Install following pip packages
```bash 
$ pip install requests
$ pip install bs4 
$ pip install lxml 
$ pip install tabulate 
$ pip install termcolor
```
3. Simple copy-paste the following in terminal for installation
```bash
$ git clone https://github.com/kryptxy/torrench.git ~/.torrench
# Create symlink
$ mkdir $HOME/.torrench/bin && ln -s $HOME/.torrench/data/torrench.py $HOME/.torrench/bin/torrench
# Make executable
$ chmod a+x $HOME/.torrench/data/torrench.py
# Add torrench to PATH. Change the *rc file according to shell you use
$ printf "#Torrench\nPATH=$HOME/.torrench/bin:$PATH" >> $HOME/.bashrc; source $HOME/.bashrc
```
4. That's it!

## Usage (example below)
```bash
usage: torrench [-h] [-p LIMIT] [-c] [-v] [search]

A simple torrent search tool.

positional arguments:
  search                Enter search string

optional arguments:
  -h, --help            show this help message and exit
  -p LIMIT, --page-limit LIMIT
                        Number of pages to fetch results from (1 page = 30
                        results). [default: 1]
  -c, --clear-html      Clear all torrent description HTML files and exit.
  -v, --version         Display version and exit.
  
Example: 
$ torrench -p 5 "suits s01e01" - Fetches torrents for 'suits s01e01' from first 5 pages
$ torrench "the flash s03e16" - Fetches torrents for 'the flash s01e01' from first page only
```
## Known Issues (and Workarounds)
1. Results overlap with each other
	* Workaround - **If enlarging the terminal does not solve this ofc** - (Recommended) Reduce the output parametes [In torrench.py -> alter _mylist_ and _final_output_ accordingly] OR reduce terminal font size.
2. A torrent might take very long to fetch results. I have generally faced this issue when running torrench for the first time. I still got to figure this out. Till then, here is what I do:
	* Abort the ongoing search [Ctrl+C]
	* Search again. The second time generally works fine.
### Note
* Each and every detail you will see on the terminal/HTML page is fetched from the website. If some info is missing/unintended, it's probably how its available on website.
* An important note about **comments** - The comments in torrent website are divided into pages. By default, torrent website displays the **most recent** comments, that is, the _last_ comments page. That is how it's fetched by the tool as well.
Example: If a torrent has 100 comments, and the comments are divided into 4 pages, the comments available on _4th page_ are only fetched. For some reason, the comments on previous pages are not being loaded by website itself. Thus, they are not being fetched by tool.

## Disclaimer
This tool only fetches torrent and details from already existing torrent website(s). (thepiratebay proxy site(s)). I do not take any responsibility for availability of any kind of torrent data, or/and hosting of any torrent website(s). Also, I am  not responsible for closing of any of the torrent website(s). As long as the website(s) (proxies) are available, data will be fetched. The day website(s) (proxies) goes down, the tool becomes in-effective.

## Bug Report
Found a bug? Please report and help improving this tool. You can [Open Issue](https://github.com/kryptxy/torrench/issues/new) or contact me directly.

## Feedback/Suggestions/Feature Requests 
Feedbacks are much appreciated. They help in improving the tool, and keep me motivated. 

I am open to suggestions/feature requests. Please [Open Issue](https://github.com/kryptxy/torrench/issues/new)
or contact me directly.

## Contact
E-mail : kryptxy@protonmail.com

## Licence
```
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Kernel Adiutor.  If not, see <http://www.gnu.org/licenses/>.
```
