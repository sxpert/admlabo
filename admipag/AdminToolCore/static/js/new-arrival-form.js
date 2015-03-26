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
		var sel = parseInt($(ev.target.selectedOptions[0]).val());
		if (sel == 9) {
			
		} else {
			
		}
	});
});
