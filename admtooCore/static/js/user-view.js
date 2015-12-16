$('#regen-dirs').on('click', function (event) {
	do_it = confirm('Êtes vous sûr de vouloir re-créer les répertoires de l\'utilisateur ?');
	if (do_it) {
		var url = window.location.pathname;
		url += 'action/dirs/regen';
		df_ajax('GET', url, null , function() {
			alert('les répertoires de l\'utilisateur ont été créés à nouveau');
		});
	}
	event.preventDefault();
});

$('#destroy-user').on('click', function (event) {
    do_it = confirm('Êtes vous sûr de vouloir détruire les données de l\'utilisateur ?');
    if (do_it) {
        var url = window.location.pathname;
        url += 'action/user/destroy';
        df_ajax('GET', url, null , function() {
            alert('les données de l\'utilisateur ont été supprimées');
			// generate update calls
			df_update_fields ('userclass,main-team,secondary-teams,mailing-lists,groups');
        });
    }
    event.preventDefault();
});

