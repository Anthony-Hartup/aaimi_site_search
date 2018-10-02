// AAIMI SITE SEARCH 
/// EMBED CODE

// Javascript
//Paste the following block of code anywhere in your main Javascript file

///////// START AAIMI SiteSearch code
// Show the search box when user clicks Site Search button
$('button#showaaimisearch').click(function (e) {
	$('#mainsearcharea').attr('style', 'display:block');
	$('#hide_aaimi_search').attr('style', 'display:block');
	$('#show_aaimi_search').attr('style', 'display:none');
});
// Hide the search box when user clicks Hide Search button
$('button#hideaaimisearch').click(function (e) {
	$('#mainsearcharea').attr('style', 'display:none');
	$('#hide_aaimi_search').attr('style', 'display:none');
	$('#show_aaimi_search').attr('style', 'display:block');
});
// Send search terms to PHP/Python and display results
$('#aaimisearchform').submit(function(event) {
	event.preventDefault();
    var $form = $( this ),
    	searchterms = $form.find( "input[name='searchterms']" ).val();
	$.post('/aaimi_site_search/site_search.php', {'searchterms':searchterms}, function(data) {		
		document.getElementById("mainresults").innerHTML = data;
	});    	    	
});
////// END SiteSearch code
