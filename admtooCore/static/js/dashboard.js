function load_block (block, sort=undefined) {
	// attempt to get block data
	var url = window.location.pathname+block;
	if (sort !== undefined) {
		url+='?sort='+sort
	}
	$.ajax ({
		'url': url,
		'success':	function (data) {
						var div = $('#'+block);
						div.html(data);
						var h1 = div.find('h1');
						var h = div.innerHeight() - h1.height();
						var content = div.find('.table-scroller');
						content.css('max-height', h);
					},
		'datatype': 'html'
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.log (jqXHR.status);
		console.log (textStatus);
		console.log (errorThrown);
	});
}

function load_blocks (blocks) {
	blocks.forEach(function (block) {
		load_block (block);
	});
}

$(function () {
	load_blocks (['DBNewArrivals','DBUnknownUsers']);
});
