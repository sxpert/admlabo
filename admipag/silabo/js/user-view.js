function icon_path (icon) {
	return '/static/material-design-icons/'+icon+'.svg';
}

function icon_button (icon, func) {
	var button = $('<img src="'+icon_path(icon)+'" style="float:right" data-control="button"/>');
	// attach the event
	button.on('click', func);
	return button;
}

function df_initialize (index, elem) {
	var field = $(elem).attr('data-field');
	var  type = $(elem).attr('data-type');
	df_set_edit_icon ($(elem))
};

function data_field (event) {
	var target = event.target;
	return $($(target).parents('[data-field]')[0]);
}

function df_set_edit_icon (elem) {
	var data_control = elem.find('[data-control]')
	console.log ('set_edit_icon', data_control);
	data_control.remove();
	elem.prepend(icon_button('content/svg/design/ic_create_24px',df_start_edit));
} 

function df_set_save_icons (elem) {
	elem.find('[data-control]').remove();
	elem.prepend(icon_button('content/svg/design/ic_save_24px', df_save_edit));
	elem.prepend(icon_button('content/svg/design/ic_clear_24px', df_clear_edit));
}

function df_start_edit (event) {
	var p = data_field (event);
	df_set_save_icons(p)
	p.children().not('[data-control]').remove();
	df_get_data (p);
} 

function df_save_edit (event) {
	var p = data_field(event);
	df_save_value(p);
}

function df_clear_edit (event) {
	var p = data_field(event);
	df_set_edit_icon(p);
	df_set_value(p);
}

function df_ajax (method, url, data, callback) {
	var csrftoken = $.cookie ('csrftoken');
	$.ajaxSetup ({
		beforeSend: function (xhr, settings) {
			xhr.setRequestHeader ('X-CSRFToken', csrftoken);
		},
	});
	$.ajax ({
		'type':		method,
		'dataType':	'json',
		'url':		url,
		'data':		data,
		'success':	callback,
	});	
}

function df_get_data (field) {
	var f_type = field.attr('data-type');
	var f_name = field.attr('data-field');
	var url = window.location.pathname;
	url += 'options/'+f_type+'/'+f_name;
	df_ajax ('GET', url, null, 
		function (result) {
			console.log(result);
			switch (f_type) {
				case 'multiselect': df_multiselect_initialize (field, result); break;
				case 'select': df_select_initialize (field, result); break;
			}
		});
}

function df_save_value (field) {
	var f_type = field.attr('data-type');
	var f_name = field.attr('data-field');
	var url = window.location.pathname;
	url += 'value/'+f_type+'/'+f_name;
	var data = null;
	switch (f_type) {
		case 'select': 
			var control = field.find('[data-control=select]');
			// only one option selected
			var sel = parseInt($(control[0].selectedOptions[0]).val());
			data = { 'value': sel };
			break;
	}
	data = JSON.stringify (data);
	df_ajax ('POST', url, data,
		function (result) {
			df_set_edit_icon(field);
			switch (f_type) {
				case 'select': df_select_set_value (field, result); break;
			}
		});
}

function df_set_value (field) {
	var f_type = field.attr('data-type');
	var f_name = field.attr('data-field');
	var url = window.location.pathname;
	url += 'value/'+f_type+'/'+f_name;
	df_ajax ('GET', url, null,
		function (result) {
			switch (f_type) {
				case 'multiselect' : df_multiselect_set_value (field, result); break;
				case 'select': df_select_set_value (field, result); break;
			}
		});
}

/******************************************************************************
 *
 * spécifique a chaque datafield type
 *
 */

/* 
 * multiselect type field
 */

function df_multiselect_initialize (field, data) {
	var opt = data['options'];
	var sel = data['selected'];
	// generate selected list
	var u = $('<ul data-control="selected-list"/>');
	var sopt = [];
	for (var key in sel) {
		key = sel[key];
		sopt.push ([key, opt[key]]);
	}
	sopt.sort (function (a, b) { return a[1] > b[1]; });
	for (var o in sopt) {
		var key = sopt[o][0];
		var val = sopt[o][1];
		var l = $('<li data-value="'+key+'">'+val+'</li>');
		// remove button
		var b = icon_button ('content/svg/design/ic_remove_24px', df_multiselect_remove_option);
		l.prepend(b);
		u.append(l);
	}
	// generate options list	
	sopt = [];
	for (var key in opt) {
		var val = opt[key]; 
		sopt.push ([key, val]);
	} 
	sopt.sort (function (a, b) { return a[1] > b[1]; });
	var d = $('<div data-control="select-div"/>');
	var b = icon_button ('content/svg/design/ic_add_24px', df_multiselect_add_option);
	d.append (b);
	var s = $('<select data-control="select-control">');
	// add options in the select
	for (var key in sopt) {
		var k = sopt[key][0];
		var v = sopt[key][1];
		if ($.inArray(parseInt(k), sel)==-1) {
			var o = $('<option value="'+k+'">'+v+'</option>');
			s.append (o);
		}
	}
	d.append (s);
	// append controls
	field.append(u);
	field.append(d);
}

function df_multiselect_remove_option (event) {
	var field = data_field (event);
	var option = $($(event.target).parents('[data-value]')[0])
	var key = option.attr('data-value');
	var value = option.text();
	var select = field.find('[data-control=select-control]');
	var list = select.children();
	var newitem = $('<option value="'+key+'">'+value+'</option>');
	var found = false;
	for (var i=0; i<list.length; i++) {
		var item = $(list[i]);
		if (value < item.text()) {
			newitem.insertBefore(item);
			found = true;
			break;
		}
	}
	if (! found) select.append(newitem);
	option.remove();
}

function df_multiselect_add_option (event) {
	var field = data_field (event);
	// get option values
	var control = field.find('[data-control=select-control]');
	var sel = $(control[0].selectedOptions[0]).val();
	if (sel===undefined) return;
	sel = parseInt(sel);
	var opt = control.find('[value='+sel+']');
	var key = opt.attr('value');
	var value = opt.text();
	opt.remove()
	// insert the value into the list of things
	var control = $('[data-control=selected-list]');
	var list = control.children();
	var newitem = $('<li data-value="'+key+'">'+value+'</li>');
	var b = icon_button ('content/svg/design/ic_remove_24px', df_multiselect_remove_option);
	newitem.prepend(b);
	var found = false;
	for (var i=0; i<list.length;i++) {
		var item = $(list[i]);
		if (value < item.text()) {
			newitem.insertBefore(item);	
			found = true;
			break;
		}
	}
	if (! found) control.append(newitem);
}

function df_multiselect_set_value (field, data) {
}

/*
 * select type field
 */
 
function df_select_initialize (field, data) {
	var s = '<select data-control="select">';
	var opt = data['options']
	var sel = data['selected']
	var topt = [];
	for (var key in opt) topt.push([key, opt[key]]);
	topt.sort(function(a, b) { return a[1] > b[1]; });
	for (opt in topt) {
		var key = topt[opt][0];
		var val = topt[opt][1];
		s+='<option value="'+key+'"';
		if (parseInt(key)==sel) s+=' selected';
		s+='>'+val+'</option>';
	}
	s+='</select>';
	field.append($(s))
}

function df_select_set_value (field, data) {
	var val = $('<a href="'+data['url']+'">'+data['value']+'</a>');
	field.append (val);
}

/*
 * spécifique a la user-view
 *
 */

$(function(){
	$('[data-field]').each(df_initialize);
});
