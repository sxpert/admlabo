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
	var type = $(elem).attr('data-type');
	var edit = $(elem).attr('data-edit');
	df_set_value ($(elem));
	if ((edit===undefined)|(edit!="no")) {
		df_set_edit_icon ($(elem));
	}
};

function data_field (event) {
	var target = event.target;
	return $($(target).parents('[data-field]')[0]);
}

function df_set_edit_icon (elem) {
	var data_control = elem.find('[data-control]')
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
		'processData': false,
		'contentType': false,
		'success':	callback,
	});	
}

function df_get_data (field, callback=undefined) {
	var f_type = field.attr('data-type');
	var f_name = field.attr('data-field');
	var url = window.location.pathname;
	url += 'options/'+f_type+'/'+f_name;
	df_ajax ('GET', url, null, 
		function (result) {
			if (callback!==undefined) 
				return callback(field, result);
			switch (f_type) {
				case 'multiselect': df_multiselect_initialize (field, result); break;
				case 'select': df_select_initialize (field, result); break;
				case 'text' : df_text_initialize (field, result); break;
				case 'multitext': df_multitext_initialize (field, result); break;
				case 'photo': df_photo_initialize (field, result); break;
			}
		});
}

function df_save_value (field) {
	var f_type = field.attr('data-type');
	var f_name = field.attr('data-field');
	var f_update = field.attr('data-update');
	var url = window.location.pathname;
	url += 'value/'+f_type+'/'+f_name;
	var data = null;
	switch (f_type) {
		case 'multiselect': data = df_multiselect_get_value (field); break;
		case 'select': data = df_select_get_value (field); break;
		case 'text': data = df_text_get_value (field); break;
		case 'multitext': data = df_multitext_get_value (field); break;
		case 'photo': data = df_photo_get_value (field); break;
	}
	// handle uploading binary files too
	if ('_is_formdata' in data) {
		if ('_formdata' in data) {
			data = data['_formdata'];
		} else {
			console.log ('ERROR: can\'t find FormData object');
			data = {};
		}
	} else {
		data = JSON.stringify (data);
	}
	df_ajax ('POST', url, data,
		function (result) {
			console.log (result);
			var e = ('errors' in result);
			if (!e) 
				df_set_edit_icon(field);
			switch (f_type) {
				case 'multiselect': df_multiselect_set_value (field, result); break;
				case 'select': df_select_set_value (field, result); break;
				case 'text': df_text_set_value (field, result); break;
				case 'multitext': df_multitext_initialize (field, result); break;
				case 'photo' : df_photo_set_value (field, result); break;
			};
			if (!e) 
				df_update_fields (f_update);
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
				case 'display': 
				case 'text': df_text_set_value (field, result); break;
				case 'multitext' : df_multitext_initialize (field, result); break;
				case 'photo' : df_photo_set_value (field, result); break;
			}
		});
}

/*
 * update fields
 * fields is a string containing comma separated field names.
 */ 
function df_update_fields (fields) {
	if (fields===undefined) return;
	fields = fields.split(',');
	fields.forEach (function (element, index, array) {
		var e = $('[data-field='+element+']');
		e.children().not('[data-control]').remove();
		var f_type = e.attr('data-type');
		switch (f_type) {
			case 'select' : df_select_refresh (e); break;
			case 'display' : df_set_value(e); break;
			case 'multiselect' : df_multiselect_refresh (e); break;
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
//	sel = parseInt(sel);
	var opt = control.find('[value='+sel+']');
	var key = opt.attr('value');
	var value = opt.text();
	opt.remove()
	// insert the value into the list of things
	var control = field.find('[data-control=selected-list]');
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
	var values = data['values'];
	if (values===undefined) return;
	var opt = [];
	for (var i=0; i<values.length; i++)
		opt.push ([values[i]['url'], values[i]['value']]);
	opt.sort (function (a, b) { return a[1] > b[1]; });
	var s = '<ul>';
	for (var i=0; i<opt.length; i++) 
		s+='<li><a href="'+opt[i][0]+'">'+opt[i][1]+'</a></li>';
	s+='</ul>';
	field.append($(s));
}

function df_multiselect_get_value (field) {
	var control = field.find('[data-control=selected-list]');
	// list all options 
	var sel = [];
	var list = control.find('[data-value]');
	for (var i=0; i<list.length; i++)
		sel.push($(list[i]).attr('data-value'));
	var data = { 'values': sel };
	return data;
}

/* TODO: handle the case when we're currently editing this field */
function df_multiselect_refresh (field) {	
	df_set_edit_icon (field);
	df_set_value (field);	
}


/*
 * select type field
 */
 
function df_select_initialize (field, data) {
	var s = '<select data-control="select">';
	var noblank = data['noblank']; // no blank option
	var opt = data['options'];
	var sel = data['selected'];
	
	var topt = [];
	for (var key in opt) topt.push([key, opt[key]]);
	topt.sort(function(a, b) { return a[1] > b[1]; });
	// add an empty option at the begining
	if (!((noblank !== undefined) && (noblank===true)))
		topt.unshift(['','']);
	for (opt in topt) {
		var key = topt[opt][0];
		var val = topt[opt][1];
		s+='<option value="'+key+'"';
		//if (parseInt(key)==sel) s+=' selected';
		if (key==sel) s+=' selected';
		s+='>'+val+'</option>';
	}
	s+='</select>';
	field.append($(s))
}

function df_select_set_value (field, data) {
	if (!('value' in data)) return;
	var url = data['url']
	var value = data['value']
	if (url!==undefined) 
		var val = $('<a href="'+data['url']+'">'+value+'</a>');
	else	
		var val = $('<span>'+value+'</span>')
	field.append (val);
}

function df_select_get_value (field) {
	var control = field.find('[data-control=select]');
//	var sel = parseInt($(control[0].selectedOptions[0]).val());
	var sel = $(control[0].selectedOptions[0]).val();
	console.log (sel)
	if (sel.length==0)
		sel = null;
	var data;
	data = { 'value': sel };
	return data;
}

function df_select_refresh (field) {
	// step 1 : identify display mode
	var select = field.find('[data-control=select]');
	if (select.length == 0) {
		df_set_value (field);
	} else {
		df_get_data (field, function (field, data) {
			var opt = data.options;
			var noblank = data.noblank
			var topt = []
			for (var key in opt) topt.push([key, opt[key]]);
			topt.sort(function(a,b) { return a[1] > b[1]; });
			var sel = $(select[0].selectedOptions[0]).val();
			select.empty();
		    if (!((noblank !== undefined) && (noblank===true)))
		        topt.unshift(['','']);
		    for (opt in topt) {
				var key = topt[opt][0];
				var val = topt[opt][1];
				var o = $('<option>');
				o.val(key);
				o.text(val);
				if (key==sel) 
					o.attr('selected','');
				select.append(o);		
			}

		});
	}
}

/* 
 * text type field
 */

function df_text_initialize (field, data) {
	if (!('value' in data)) return;
	var f = $('<input data-control="text"/>');
	f.attr('value',data['value']);
	field.append (f);
}

function df_text_set_value (field, data) {
	if (!('value' in data)) return;
	field.append ($('<span>'+data['value']+'</span>'));
}

function df_text_get_value (field) {
	var control = field.find('[data-control=text]');
	var val = control.val();
	var data = {'value': val};
	return data;
}

/*
 * multitext type field
 */

function df_multitext_initialize (field, data) {
	console.log ('df_multitext_initialize');
	console.log (data);
	var values = data['values'];
	var errors = null;
	if ('errors' in data)
		errors = data['errors'];
	console.log (values);
	/* create or empty the existing container */
	var ul = field.find('[data-control=multitext-list]');
	if (ul.length==0)
		ul = $('<ul data-control="multitext-list">');
	else
		ul.empty();
	/* generate the entries */
	for (var k in values) {
		console.log (k);
		var li = $('<li data-control="multitext-entry">');
		if (errors) {
			var b = icon_button ('content/svg/design/ic_remove_24px', df_multitext_remove_option);
			var input = $('<input type="text" data-control="multitext-input">');
			input.val(values[k]);
			li.append(b);
			li.append(input);
			if (errors && (errors[k]!=null)) {
				console.log (errors[k]);
				var error = $('<img src="'+icon_path('content/svg/design/ic_report_24px')+'" data-control="button"/>');
				error.attr('title', errors[k]);
				li.append (error);
			} 
		} else 
			li.text(values[k])
		ul.append(li);
	}
	if (errors) {
		var li = $('<li data-control="multitext-append">');
		var b = icon_button ('content/svg/design/ic_add_24px', df_multitext_add_option);
		li.append(b);
		ul.append(li);
	}
	field.append (ul);
}

function df_multitext_get_value (field) {
	console.log ("df_multitext_get_value");
	var list = field.find('[data-control=multitext-input]')
	console.log (list);
	var data = {};
	var values = [];
	for (var i=0; i<list.length; i++) {
		var li = $(list[i])
		values.push (li.val());
	}
	data['values'] = values;
	console.log (data);
	return data;
}

/* remove an entry from the list
 */
function df_multitext_remove_option (e) {
	console.log ('multitext-remove-option');
	var li = $(e.target).parents('[data-control=multitext-entry]');
	li.remove();
}

/* adds an empty multitext entry
 */
function df_multitext_add_option (e) {
	console.log ('multitext-add-option');
	var mt = $(e.target).parents('[data-control=multitext-list]');
	/* generate new entry */
	var li = $('<li data-control="multitext-entry">');
	var b = icon_button ('content/svg/design/ic_remove_24px', df_multitext_remove_option);
	var input = $('<input type="text" data-control="multitext-input">');
	li.append (b);
	li.append (input);
	li.insertBefore (mt.children('[data-control=multitext-append]'));
}

/*
 *
 * photo field
 *
 */

function df_photo_create_img_element (field) {
	var img = document.createElement ('img');
	$(img).addClass('userpic');
	$(img).attr('data-control', 'image-display');
	field.append ($(img));
	return img
}

function df_photo_file_selected (event, field) {
	var element = event.target
	if (element.tagName === 'INPUT') {
		console.log (element);
		var files = element.files;
		var selectedFile = files[0]
		console.log (selectedFile);
		// the img should be already created
		var img = df_photo_create_img_element (field);
		img.file = selectedFile;
		var reader = new FileReader ();
		reader.onload = (function (aImg) { return function (e) {aImg.src = e.target.result; }})(img);
		reader.readAsDataURL (selectedFile);		
		
	} else {
		console.log ('window');
		df_set_edit_icon (field);
		df_set_value (field);	
	}
	// remove event on window
	$(window).off('focus');
}

// create the input element and add it to the field
function df_photo_create_input (field) {
	var i = $('<input data-control="file-selector" type="file" accept="image/*" style="display:none"/>');
	field.append(i);
	return i;
}

function df_photo_select_file (event, field) {
	console.log (field);
	var f = $.find('form')[0];
	// find if we have an input element.
	var i = field.find('[type=file]')[0];
	// if not, add it
	if (i===undefined) {
		i = df_photo_create_input (field);		
	}
	console.log (i);
	// register change event
	$(i).off();
	$(i).on('change', function (event) {
		var f = field;
		df_photo_file_selected (event, f);
	});
	$(window).focus(function (event) {
		var f = field;
		df_photo_file_selected (event, f);
	});
	i.click();
}

function df_photo_set_value (field, data) {
	var img = df_photo_create_img_element (field);
	
	// bind
	field.find('[data-control=button]').on('click', function (event) {
		var f = field;
		df_photo_select_file(event, f);
	});	
}

function df_photo_get_value (field) {
	console.log ('uploading file');
	var i = field.find('[type=file]')[0];
	if (i === undefined) {
		console.log ('there\'s no input field to find');
		return;
	}
	var files = i.files;
	var data = {};
	console.log (files.length);
	if (files.length==1) {
		var file = files[0];
		console.log (file);
		var fd = new FormData();
		fd.append (field.attr('data-field'), file);
		data['_is_formdata'] = true;
		data['_formdata'] = fd
	} else {
		console.log ('no files selected');
	}
	return data;
}

function df_photo_initialize (field, data) {
	var f = field.parents('form');
	var i = f.find('[type=file]')[0]
}

/*
 * spécifique a la user-view
 *
 */

$(function(){
	$('[data-field]').each(df_initialize);
});
