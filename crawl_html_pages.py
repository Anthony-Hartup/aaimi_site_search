#!/bin/bash

# AAIMI SiteSearch: CRAWLER
# Crawl a web server recursively and extract words from body and title of HTML files.
# Create a list of all word instances for use with the AAIMI SiteSearch system

# For full usage instructions visit:
# https://anthscomputercave.com/projects/aaimi/site_search/aaimi_site_search.html

# Part of the AAIMI SiteSearch system
# Version 0.1

###############

# Copyright (C) 2018  Anthony Hartup

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

###############

# Use Subprocess to perform file and folder operations 
import subprocess
# Use Operater to sort lists
import operator
# Use JSON to store word list
import json

# Words to exclude from search terms
non_words = ["the", "and", "be", "but", "from", "or", "cheers", "for", "of", "you", "your", "is", "these", "next", "I", "there", "was", "to", \
             "i'll", "have", "we", "we'll", "at", "a", "in", "it", "on", "as", "this", "my", "if", "are", "any", "am", "me", "has", \
             "so", "an", "that", "that's", "us", "what", "our", "with", "now"]

punctuation_chars = [".", '"', "#", "[", "]", "(", ")", "{", "}", ":", "=", "\n", "\\", "/", "\t", "!", "$", "&", "+"]

# An array to hold words and the number of times they appear in each file.
search_words = {}
# File to write finished word list
main_list = "word_list.txt"
#The HTML title content for each file
title_list = "page_titles.txt"

letters = {} # ???
#letters2 = {}

# The full path to the currently open file
article_identifier = ""

# A list of pages to crawl, generated on startup
pages = []

# Number of files crawled
page_count = 0

# A line that signifies when to start scraping, so you can exclude the entire header, scripts and nav-panels, etc
starting_point = "<body>"

# A unique line that signifies the end of the text to read on each page (optional)
last_line = "</body>"

# Folders to exclude from crawling (include slash after, eg: /home/public_html/myfolder/)
excluded_folders = []

#The URL for your website (include slash after, eg: https://yoururl.com/)
yoursite = "https://your_website.com/"

# The path to the web directory on your server
# Leave blank if crawl_html_pages.py is in the aaimi_site_search folder in the webroot directory
# To run crawl_html_pages.py from outside the webroot, add full path to webroot with trailing slash
webroot = ""

if webroot == "":
    # Get current directory
    cmdpipe = subprocess.Popen("pwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    raw_text = cmdpipe.stdout.readlines()
    # Remove the search folder name to get the webroot
    for text in raw_text:
        webroot = text.replace("aaimi_site_search\n", "")   

# If adding multiple web folders or sites to one search file change to yes to append to existing list
existing_list = "no"

if existing_list == "no":
    main_word_list = [{"a_j": {}, "k_z": {}, "numbers": {}, "none": {}}]
    main_title_list = [{}]
else:
    ### Open the existing JSON word list
    with open(main_list) as source_file:
        main_word_list = json.load(source_file)

    # Open the existing JSON list of titles for pages
    with open(title_list) as title_source_file:
        main_title_list = json.load(title_source_file)    


# Crawl the webroot folder recursively and create list of all html files
def get_site_pages():
    global page_count
    # Use LS to list folders and files recursively
    #comm = "cd .. && ls -R"
    comm = "cd " + webroot + " && ls -R"
    cmdpipe = subprocess.Popen(comm, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    whole_list = cmdpipe.stdout.readlines()
    # Scrape each line of the LS results for HTML filenames, keeping track of currently focused directory.
    for i in whole_list:        
        if ":" in i:
            # Not a file name, focus has moved to new folder. Remove junk from folder name and append to webroot
            current_fold = i.replace(":\n", "/")
            current_folder = webroot + current_fold.replace("./", "")
            
        elif ".html" in i:
            # HTML file, create path name and add to list
            filepath = current_folder + i
            filepath = filepath.replace("\n", "")
            # Ensure file is not in excluded directory
            include = "yes"
            for f in excluded_folders:
                if f in filepath:
                    include = "no"
            # Add to list for crawling
            if include == "yes":
                page_count += 1
                pages.append(filepath)    
    print(str(page_count) + " pages found")
    
get_site_pages()


# Extract words from the HTML text of a page, excluding everything between <tags>
def read_html(link_file):
    global non_words, article_identifier, main_word_list, last_line, letters, yoursite, starting_point, punctuation_chars
    # Open file
    file_content = open(link_file)
    file_content.seek(0)
    # Set flag to show that focus has not reached the body tag of the HTML
    status = "head_tag"
    # Array to hold words and their instances from this page
    search_words = {}
    # Build full URL for this page by replacing the webroot path with your website URL
    article_identifier = link_file.replace(webroot, yoursite)
    for line in file_content:
        # Ignore lines except title tag until head section is finished
        if status == "head_tag":
            if starting_point in line:
                # Set flag to begin reading after this line next line
                status = "not_tag"
            elif "<title>" in line:
                # Get the title of the page to display in search results
                title = line.replace("<title>", "")
                title = title.replace("</title>", "")
                title = title.replace("\t", "")
                title = title.replace("\n", "")
                if article_identifier not in main_title_list[0]:
                    main_title_list[0][article_identifier] = title                
        elif status == "not_tag": # Inside HTML body
            
            # Check that not at the target end line
            if last_line in line:
                status = "finished"
            
            # Exclude HTML tags from line and keep all other content
            if status != "finished":
                # Store characters from content of line
                new_line = ""
                for character in line:
                    if str(character) == "<":
                        # Beginning of tag, stop storing characters
                        status = "is_tag"                    
                    elif str(character) == ">":
                        # End of tag, set flag to start storing characters after this one
                        status = "end_tag"
                        
                    if status == "not_tag":
                        # Not inside a tag or at end of tag, store character
                        new_line += str(character)
                    if status == "end_tag":
                        # Set flag to start storing characters
                        status = "not_tag"
                        
                # Replace word seperators with spaces
                space_chars = ["-", "_"]
                for char in space_chars:
                    #while char in new_line:
                    new_line = new_line.replace(char, " ")
                # Remove hidden formatting
                new_line = new_line.strip()
                # Seperate line into words
                words_in_line = new_line.split(" ")
                
                               
                for word in words_in_line:                
                    # Remove unwanted characters from word
                    real_word = word.replace(",", "")
                    # Remove all other symbols
                    for current_char in punctuation_chars:
                        real_word = real_word.replace(current_char, "")
                        
                    # Remove single quotes if not used as apostrophy
                    if "'" in real_word:
                        if real_word.index("'") == 0 or real_word.index("'") == -1:
                            real_word = real_word.replace("'", "")                        
                    real_word = real_word.lower()

                    # Add or increment word in list if not in non_words array
                    if real_word not in non_words and len(real_word) > 1:
                        if real_word not in search_words:
                            # Create entry for word
                            search_words[real_word] = 1
                        else:
                            # Increment the number of instances for the word
                            search_words[real_word] += 1
    file_content.close()
    # Add page words to main word file
    for each_word in search_words:
        # Select which section to store word based-on first letter
        if ord(each_word[0]) in range(97, 107):
            first_letter = "a_j"
        elif ord(each_word[0]) in range(107, 123):
            first_letter = "k_z"
        elif ord(each_word[0]) in range(48, 58):
            first_letter = "numbers"
        else:
            first_letter = "none"
    
        # Add new entry if word not already there    
        if each_word not in main_word_list[0][first_letter]:            
            main_word_list[0][first_letter][each_word] = {}
            # Record instance of starting letter
            if each_word[0] not in letters:
                letters[each_word[0]] = 1
            else:
                letters[each_word[0]] += 1
            
        # Add URL entry for this page to word's array with number of word instances
        main_word_list[0][first_letter][each_word][article_identifier] = search_words[each_word]
    search_words = {}

# Read all pages
for webpage in pages:
    read_html(webpage)

total_words = len(main_word_list[0]["a_j"]) + len(main_word_list[0]["k_z"]) + len(main_word_list[0]["numbers"])
print("Scraped " + str(total_words) + " words from " + str(page_count) + " pages")

print("Number of words begining with each letter:")
for l in letters:
    print(str(l) + ": " + str(letters[l]))

### Write updated word and title lists
with open(main_list, 'w') as maindata:
    json.dump(main_word_list, maindata)
with open(title_list, 'w') as main_title_data:
    json.dump(main_title_list, main_title_data)



    
