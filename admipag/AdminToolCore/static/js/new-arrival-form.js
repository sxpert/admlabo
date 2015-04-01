function toggle_statut () {
	var statut = $('[name=status]');
	var sel = parseInt (statut.val());
	// get target's tr
	var er1 = $('#study_level_error');
	var tr1 = $($('[name=study_level]').parents('tr')[0]);
	var er2 = $('#ujf_student_error');
	var tr2 = $($('[name=ujf_student]').parents('tr')[0]);
	if (sel == 9) {
		er1.show(); 
		tr1.show();
		er2.show();
		tr2.show();
	} else {
		er1.hide();
		tr1.hide();
		er2.hide();
		tr2.hide();
	}
}

function toggle_office () {
	var office = $('[name=office]')
	var sel = office.val();
	var er = $('#other_office_error');
	var tr = $($('[name=other_office]').parents('tr')[0]);
	if (sel=='') {
		er.show();
		tr.show();
	} else {
		er.hide();
		tr.hide();
	}
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
	$("[name=status]").change(function(ev) {
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
