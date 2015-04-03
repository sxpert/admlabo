function load_blocks (blocks) {
	blocks.forEach(function (block) {
		// attempt to get block data
		var url = window.location.pathname+block;
		console.log (url);
		$.ajax ({
			'url': url,
			'success':	function (data) {
					    	console.log (data);
							var div = $('#'+block);
							console.log (div);
							div.html(data);
						},
			'datatype': 'html'
		}).fail(function(jqXHR, textStatus, errorThrown) {
			console.log (jqXHR.status);
			console.log (textStatus);
			console.log (errorThrown);
		});
	});
}

$(function () {
	load_blocks (['DBNewArrivals']);
});
