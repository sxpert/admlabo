function toggle_statut () {
	var statut = $('[name=statut]');
	var sel = parseInt (statut.val());
	// get target's tr
	var target_tr = $(statut.parents('tr')[0]);
	var tr1 = target_tr.next('tr');
	var tr2 = tr1.next('tr')
	if (sel == 9) {
		tr1.show();
		tr2.show();
	} else {
		tr2.hide();
		tr1.hide();
	}
}

function toggle_office () {
	var office = $('[name=office]')
	var sel = office.val();
	var tr = $(office.parents('tr')[0]).next('tr')
	if (sel=='') 
		tr.show();
	else
		tr.hide();
}

function toggle_os_type () {
	var os_type = $('[name=os_type]')
	var sel = os_type.val();
	var tr = $(os_type.parents('tr')[0]).next('tr')
	if (sel=='0') 
		tr.show();
	else
		tr.hide();
}

$(function() {
	$("[name=birthdate]").datepicker({
		showOn: "button",
		buttonImage: "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		yearRange: "-80:-10",
		changeYear: true,
		defaultDate: "-18y",
		dateFormat: "yy-mm-dd",
	});
	$("[name=statut]").change(function(ev) {
		toggle_statut();
	});
	$('[name=office]').change(function(ev) {
		toggle_office();
	});
	toggle_statut();
	toggle_office();
	$("[name=arrival]").datepicker({
		showOn: "button",
		buttonImage: "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		changeYear: true,
		dateFormat: "yy-mm-dd",
	});
	$("[name=departure]").datepicker({
		showOn: "button",
		buttonImage: "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		changeYear: true,
		dateFormat: "yy-mm-dd",
	});
	$('[name=os_type]').change(function(ev) {
		toggle_os_type();
	});
	toggle_os_type();
});
