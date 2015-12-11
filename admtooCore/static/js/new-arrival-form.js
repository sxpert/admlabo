function toggle_statut () {
	var statut = $('[name=status]');
	var sel = parseInt (statut.val());
	// get target's tr
	var er1 = $('#study_level_error');
	var tr1 = $($('[name=study_level]').parents('tr')[0]);
	var er2 = $('#ujf_student_error');
	var tr2 = $($('[name=ujf_student]').parents('tr')[0]);
	if (statut.find('[value='+sel.toString()+']').attr('data-probie')=='true') {
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

function toggle_comp_account () {
	var comp_account = $('[name=comp_account]:checked');
	var val = comp_account.val();
    var os_type = $('[name=os_type]');
    var specific_os = $('[name=specific_os]');
    var comp_purchase = $('[name=comp_purchase]');
	var os_lang = $('[name=os_lang]');
	var tr1 = $(os_type.parents('tr')[0]);
    var tr2 = $(specific_os.parents('tr')[0]);
    var tr3 = $(comp_purchase.parents('tr')[0]);
	var tr4 = $(os_lang.parents('tr')[0]);
    if (val=='0') {
        tr1.hide();
        tr2.hide();
        tr3.hide();
		tr4.hide();
	} else {
        tr1.show();
		toggle_os_type();
		tr3.show();
		tr4.show();
	}
}
function toggle_os_type () {
	var os_type = $('[name=os_type]');
	var sel = os_type.val();
	var tr = $(os_type.parents('tr')[0]).next('tr');
	if (sel=='0')
		tr.show();
	else
		tr.hide();
}

function check_presence_period () {
	var show = true;
	// get both dates
	var a = $('[name=arrival]').val().trim();
	var d = $('[name=departure]').val().trim();
	// check if one of the dates is empty
	if ((a.length>0)&&(d.length>0)) {
		// check if dates are in the right order
		var da = new Date(a);
		var dd = new Date(d);
		if (da>dd) 
			alert ('Il y a un probleme dans vos dates:\nLa date de départ est antérieure a la date d\'arrivée');
		else {
			// calculate length of time period in days. date difference is in ms
			var diff = (dd - da) / 86400000;
			if (diff < 21) 
				show = false;
		}
	}
	var infosys = $($('#infosys')[0]);
	var infosys_info = $($('#infosys-info')[0]);
	var infosys_warn = $($('#infosys-warn')[0]);
	if (show) {
		infosys.show();
		infosys_info.show();
		infosys_warn.hide();
	} else {
		// difference is less than 3 weeks. no account can be produced
		infosys.hide();
		infosys_info.hide();
		infosys_warn.show();
	}
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
		showOn:          "button",
		buttonImage:     "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		changeYear:      true,
		dateFormat:      "yy-mm-dd",
		onSelect:        check_presence_period,
	}).on('change', check_presence_period);
	$("[name=departure]").datepicker({
		showOn:          "button",
		buttonImage:     "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		changeYear:      true,
		dateFormat:      "yy-mm-dd",
		onSelect:        check_presence_period,
	}).on('change', check_presence_period);
	$('[name=os_type]').change(function(ev) {
		toggle_os_type();
	});
	toggle_os_type();
    $('[name=comp_account]').click(function(ev) {
        toggle_comp_account();
    });
	check_presence_period();
});
