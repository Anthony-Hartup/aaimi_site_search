<?php 
// Call the AAIMI Site Search Python program with the search terms as parameters. 
// It will return a HTML-formatted list of pages containing the most instances of the search terms
$terms = $_POST['searchterms'];
// Comment out the following two lines to call the Python program in a custom location
$dir = exec("pwd");
$command = "python " . $dir . "/site_search.py " . $terms;
// Uncomment the following two lines to call the Python program in a custom location. Change home/to/path to full path.
//$command = "python /home/path/to/site_search.py " . $terms;
system($command);
?>
