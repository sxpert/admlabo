function get_statut () {
	return parseInt ($('[name=statut]').val());
}

$(function() {
	$(".hasDatePicker").datepicker({
		showOn: "button",
		buttonImage: "/static/material-design-icons/action/svg/design/ic_event_24px.svg",
		buttonImageOnly: true,
		yearRange: "-80:-10",
		changeYear: true,
		defaultDate: "-18y",
		dateFormat: "yy-mm-dd",
	});
	$("[name=statut]").change(function(ev) {
		var sel = get_statut();
		// get target's tr
		var target_tr = $($(ev.target).parents('tr')[0]);
		var tr1 = target_tr.next('tr');
		var tr2 = tr1.next('tr')
		if (sel == 9) {
			tr1.show();
			tr2.show();
		} else {
			tr2.hide();
			tr1.hide();
		}
	});
});
