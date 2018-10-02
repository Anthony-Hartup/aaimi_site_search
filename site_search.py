#!/bin/bash

# AAIMI SiteSearch: SEARCHER
# Search a list of words for search terms and return the page URLs with the most instances of those terms

# For full usage instructions visit:
# https://anthscomputercave.com/projects/aaimi/site_search/aaimi_site_search.html

# Part of the AAIMI SiteSearch system

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

# Use Operater to sort lists
import operator
# Use JSON to parse word lists
import json
# Use Sys to get search terms from PHP
import sys
# Example call to this program from PHP:
## python site_search.py word1 word2

# Use Time to calculate how long the total search takes
import time
start_time = time.time()

# You first need to create the two files below below by running crawl_html_pages.py
# A list of all words (lower-case) on the site 
main_list = "word_list.txt"

#The HTML title content for each file
title_list = "page_titles.txt"

# Store URLs for pages containing the search terms
page_store = {}

# Flag to indicate whether a search term has been found in the word list
found = "no"

# The number of pages to display in the results
num_results_to_show = 20

# Open the word list with the number of instances of words in each page
# Looks like:  [{'word':{'page1.html':2,'page2.html':4,}, 'word2': {'page1.html':1}}]
with open(main_list) as source_file:
    main_word_list = json.load(source_file)

# Open the list of HTML titles for pages
# Looks like:  [{'page1.html':'Title for page','page2.html': 'Title for another page',}]
with open(title_list) as title_source_file:
    main_title_list = json.load(title_source_file)


# Check if a search-term is in the word list and store the URLs for the pages that feature the word, and the number of instances
def search_main_list(word):
    global page_store, found
    # Check exact word first
    # Choose which section of word list based on first letter
    if ord(word[0]) in range(97, 107):
        first_letter = "a_j"
    elif ord(word[0]) in range(107, 123):
        first_letter = "k_z"
    elif ord(word[0]) in range(48, 58):
        first_letter = "numbers"
    else:
        first_letter = "none"
        
    if word in main_word_list[0][first_letter]:
        # Word found, list the URLs that feature the word
        found = "yes"
        for pge in main_word_list[0][first_letter][word]:
            # Add to URL list or increment matches by new value
            if pge not in page_store:
                page_store[pge] = main_word_list[0][first_letter][word][pge]
            else:
                page_store[pge] += main_word_list[0][first_letter][word][pge]
                
    # Check plural version of word if not ending with s            
    if word[-1] != "s": 
        plural_word = word + "s"
        if plural_word in main_word_list[0][first_letter]:
            found = "yes"
            for pge in main_word_list[0][first_letter][plural_word]:
                # Add to URL list or increment matches by new value
                if pge not in page_store:
                    page_store[pge] = main_word_list[0][first_letter][plural_word][pge]
                else:
                    page_store[pge] += main_word_list[0][first_letter][plural_word][pge]
    # Check non plural version of word if ending in s                
    else:
        non_plural_word = word[0:-1]
        if non_plural_word in main_word_list[0][first_letter]:
            found = "yes"
            for pge in main_word_list[0][first_letter][non_plural_word]:
                # Add to URL list or increment matches by new value
                if pge not in page_store:
                    page_store[pge] = main_word_list[0][first_letter][non_plural_word][pge]
                else:
                    page_store[pge] += main_word_list[0][first_letter][non_plural_word][pge]  


# Check all search terms and compile the results
def check_words():
    global found, page_store, num_results_to_show
    # Python call will look something like:  python site_search.py word1 word2
    if len(sys.argv) > 1:
        # Get search terms from Python call and search for terms
        for search_word in sys.argv[1:]:
            if len(search_word) > 1:
                search_main_list(search_word.lower())
            
        if found == "yes":
            # Sort list by number of instances of search terms in each page (Highest to lowest)
            sorted_pages = sorted(page_store.items(), key=operator.itemgetter(1), reverse=True)
            result_count = 0
            # Create HTML to display results
            result_html = ""
            for page in sorted_pages:
                # Show only the ten best reults
                if result_count < num_results_to_show:
                    # Display the page title (if present) and the number of times the words appear in the page
                    if page[0] in main_title_list[0]:
                        result_html += "<div style='border-width:2px;border-style:solid;border-color:black;border-radius:10px;'><p style='font-size:1.1em;margin-bottom:0px;'>" + main_title_list[0][page[0]] + ": " + str(page[1]) + " word matches</p>"
                    else:
                        result_html += "<p>No title: " + str(page[1]) + "word matches</p>"
                    result_count += 1
                    # Display the full URL for the page with a link
                    result_html += "<p style='word-wrap:break-word;margin-top:0px;'><a style='font-size:.8em;' href='" + page[0] + "'>" + page[0] + "</a></p></div>"
            result_html = "<p>Found " + str(len(sorted_pages)) + " pages in " + str(round(time.time() - start_time, 2)) + " seconds</p>" + result_html
            # Send to PHP
            print(result_html)
        else:
            print("Not Found")
        page_store = {}
       
check_words()


            
        
    
                      
