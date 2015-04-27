function update_ldap_user () {
	var uid = $('[name=ldap_user]').val(); 
	var patharray = window.location.pathname.split('/');
	patharray[patharray.length-1]='userinfo';
	patharray.push(uid.toString());
	var url = patharray.join('/');
    var csrftoken = $.cookie ('csrftoken');
    $.ajaxSetup ({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader ('X-CSRFToken', csrftoken);
        },
    });
    $.ajax ({
        'type':     'get',
        'url':      url,
        'success':  function (result) {
			var select = $('[name=ldap_user]');
			var table = $(select.parents('table')[0]);
			var tbody = $(table.children('tbody')[0]);
			tbody.html(result);
		},
    });

}

$(function() {
	$('[name=ldap_user]').change(update_ldap_user);	
	update_ldap_user();
});
