<?php 
// Call the AAIMI Site Search Python program with the search terms as parameters. 
// It will return a HTML-formatted list of pages containing the most instances of the search terms
$terms = $_POST['searchterms'];
$dir = exec("pwd");
$command = "python " . $dir . "/site_search.py " . $terms;
system($command);
?>
