# aaimi_site_search
<h2>Overview</h2>
<p>This  is a drop-in search-box system that runs on your site, without redirecting your visitors or collecting their personal data. It uses no third-party search providers.</p>
<p>You simply configure and run crawl_html_pages.py to create a word list, which contains every unique word on your site and the number of instances in each page.</p>
<p>You then embed the HTML search box code into your pages, and add the Javascript code to your existing Javascript file.</p>
<p>When a visitor enters search terms they will see results for pages with the most instances of the search terms.</p>
<h2>Limitations</h2>
<p>In this version the word-list is created server-side, it is not a web-based crawler. This means it currently only indexes static content. We are adding a web-based crawler to work alongside the server-side crawler to get dynamic content.</p>
<h2>Usage</h2>
<p>You'll find full setup and usage instructions <a href="https://anthscomputercave.com/projects/aaimi/site_search/aaimi_site_search_tutorial.html" target="_blank">in the AAIMI SiteSearch tutorial at Anth's Computer Cave</a>.</p>
<p>There you can also try out the search functionality, the system is deployed across all pages on the site.</p>
<h2>Upcoming features.</h2>
<p>The system is purely word-based at the moment. It works suprisingly well on my site with around 140 articles. It aleady knows the site better than I do.</p>
<p>Using just word-repetition may not always return the most relevant results, however, because it lacks context. We are now adding methods that also focus on sentence-structure. More on this soon</p>
