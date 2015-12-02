$('#regen-dirs').on('click', function (event) {
	do_it = confirm('Êtes vous sûr de vouloir re-créer les répertoires de l\'utilisateur ?');
	if (do_it) {
		var url = window.location.pathname;
		url += 'action/dirs/regen';
		df_ajax('GET', url, null , function() {
			alert('done');
		});
	}
	event.preventDefault();
});
