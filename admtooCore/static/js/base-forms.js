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
	var ec = elem.attr('data-edit-controls');
	if ((ec!==undefined)&&((ec=="false")||(ec=="0"))) 
		return;
	elem.find('[data-control=button]').remove();
	elem.prepend(icon_button('content/svg/design/ic_create_24px',df_start_edit));
} 

function df_set_save_icons (elem) {
	var ec = elem.attr('data-edit-controls');
	if ((ec!==undefined)&&((ec=="false")||(ec=="0"))) 
		return;
	elem.find('[data-control=button]').remove();
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

function df_ajax (method, url, data, success, fail=undefined) {
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
		'success':	success,
		'error' : fail,
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
				case 'key-value' : df_keyvalue_edit_mode (field, result); break;
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
		case 'key-value': data = df_keyvalue_get_values (field); break;
		case 'photo': data = df_photo_get_value (field); break;
		case 'checkbox': data = df_checkbox_get_value (field); break;
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
	error = undefined;
	switch (f_type) {
		case 'photo' : 
			error = function (x,s,e) {
				df_photo_handle_error (field, x, s, e);
			}; 
			break;
	}
	df_ajax ('POST', url, data,
		function (result) {
			//console.log (result);
			var e = ('errors' in result);
			if (!e) 
				df_set_edit_icon(field);
			switch (f_type) {
				case 'multiselect' : df_multiselect_set_value (field, result); break;
				case 'select'      : df_select_set_value (field, result); break;
				case 'text'        : df_text_set_value (field, result); break;
				case 'multitext'   : df_multitext_initialize (field, result); break;
				case 'key-value'   : df_keyvalue_set_value (field, result); break;
				case 'photo'       : df_photo_set_value (field, result); break;
			};
			if (!e) 
				df_update_fields (f_update);
		}, error);
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
				case 'select'      : df_select_set_value (field, result); break;
				case 'display'     : 
				case 'text'        : df_text_set_value (field, result); break;
				case 'multitext'   : df_multitext_initialize (field, result); break;
				case 'key-value'   : df_keyvalue_set_value (field, result); break;
				case 'photo'       : df_photo_set_value (field, result); break;
				case 'checkbox'    : df_checkbox_set_value (field, result); break;
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
	
	var ts = '<select data-control="select-control">';
	var k, v, key, o;
	for (key in sopt) {
		k = sopt[key][0];
		v = sopt[key][1];
		if (sel.indexOf(parseInt(k))==-1) {
			ts+='<option value="'+k+'">'+v+'</option>';
		}
	}
	ts+='</select>';
	var s=$(ts);

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
	field.find('[data-control=selected-list]').remove();
	field.find('[data-control=select-div]').remove();
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
	field.find('[data-control=select]').remove();
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
	//console.log (sel)
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
	field.find('[data-control=text]').remove();
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
	//console.log ('df_multitext_initialize');
	//console.log (data);
	var values = data['values'];
	var errors = null;
	if ('errors' in data)
		errors = data['errors'];
	//console.log (values);
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
 * key-value field
 *
 */

function df_keyvalue_get_table (field) {
	var t = field.find('[data-control=kv-table]');
	if (t.length == 0) {
		t = $('<table data-control="kv-table">');
		// add table to field
		field.append(t);
	}
	return t;
}

function df_keyvalue_get_row (table, key) {
	var rows = table.find('tr[data-key]');
	var r = undefined;
	if (rows.length != 0) {
		// find the row
		for (var i=0; i<rows.length;i++) {
			var row = $(rows[i]);
			var row_key = row.attr('data-key');
			if (row_key == key) {
				r = row;
				break;	
			}
		}
	}
	if (r===undefined) {
		r = $('<tr>');
	    r.attr('data-key',key);
		h = $('<th>');
		h.text(key);
		r.append(h);
		d = $('<td>');
		r.append(d);
		// append
		var inserted = false;
		if (rows.length!=0) {
			for (var i=0; i<rows.length; i++) {
				var row = $(rows[i]);
				var row_key = row.attr('data-key');
				if (key<row_key) {
					r.insertBefore(row);
					inserted = true;
					break;
				}
			}
		}
		if (!inserted) table.append(r);
	}
	return r;
}

function df_keyvalue_add_item_to_select (select, key, name) {
	var options = select.find('option');
	for (var i=0; i<options.length;i++) if ($(options[i]).attr('value')==key) return;
	// create option
	var option = $('<option>');
	option.attr('value', key);
	option.text(name);
	// insert option
	for (var i=0; i<options.length;i++) {
		var o = $(options[i]);
		var ov = o.attr('value');
		if (key<ov) {
			option.insertBefore(o);
			return;
		}
	}
	select.append(option);
}

function df_keyvalue_remove_unused_items_from_select (select, used_keys) {
	var options = select.find('option');
	for (var i=0; i<options.length; i++) {
		var o = $(options[i]);
		var v = o.attr('value');
		if (used_keys.indexOf(o.attr('value'))!=-1) {
			o.remove();
		}
	}
}

function df_keyvalue_update_available_keys (select) {
	var i = 0;
	var table = $(select.parents('table')[0]);
	var keydata = table.attr('data-keys');
	var keys = JSON.parse(keydata);
	var usedkeys = table.find('[data-key]');
	var uk = []
	for (i=0; i<usedkeys.length;i++) uk.push($(usedkeys[i]).attr('data-key'));
	var ak = [];
	var k = Object.keys(keys);
	k.sort();
	for (i=0; i<k.length;i++) if (!(k[i] in uk)) ak.push(k[i]);
	for (i=0; i<ak.length;i++) df_keyvalue_add_item_to_select(select, ak[i], keys[ak[i]]);
	df_keyvalue_remove_unused_items_from_select(select, uk);
	var options = select.find('option');
	var tfoot = $(select.parents('tfoot')[0]);
	if (options.length==0) tfoot.hide();
	else tfoot.show();
}

function df_keyvalue_add_footer (table, keys) {
	//step 1 : add the list of keys to the table 
	table.attr('data-keys', JSON.stringify(keys));
	var footer = $('<tfoot>');
	var row = $('<tr>');
	var cell = $('<td>');
	cell.attr('colspan', '2');
	var select = $('<select>');
	cell.append(select);
	var button = icon_button ('content/svg/design/ic_add_24px', df_keyvalue_add_key);
	cell.append(button)
	row.append(cell);
	footer.append(row);
	table.append(footer);
	df_keyvalue_update_available_keys (select);
}

// read only mode
function df_keyvalue_set_pair_ro (table, key, value) {
	var r = df_keyvalue_get_row(table, key);
	var d = r.find('td');
	d.empty();
	d.text(value);
}

function df_keyvalue_set_pair_rw (table, key, value) {
	var r = df_keyvalue_get_row(table, key);
	var d = r.find('td');
	d.empty()
	var i = $('<input>');
	i.attr('type', 'text');
	i.attr('value', value);
	d.append(i);
	var button = icon_button ('content/svg/design/ic_remove_24px', df_keyvalue_delete_key);
	d.append(button);
}

function df_keyvalue_add_key (event) {
	// obtain selected key from select
	var target = $(event.target);
	var select = $(target.parents('td')[0]).find('select');
	var table = $(target.parents('table')[0])
	var selected = $(select.find(':selected')[0]);
	df_keyvalue_set_pair_rw (table, selected.attr('value'), '');
	df_keyvalue_update_available_keys(select);	
}

function df_keyvalue_delete_key (event) {
	var target = $(event.target);
	var select = $($(target.parents('table')[0]).find('select')[0]);
	var row = $(target.parents('tr')[0]);
	row.remove();
	df_keyvalue_update_available_keys(select);
}

function df_keyvalue_set_value (field, data) {
	// part 1: get all keys in a sorted array
	var val = data['values'];
	var k = Object.keys(val);
	k.sort();
	// part 2: insert all visible controls
	var t = df_keyvalue_get_table(field);
	for (var i=0; i<k.length;i++)
		df_keyvalue_set_pair_ro (t, k[i], val[k[i]]);
	// part 3: remove all keys not there
	var rows = field.find('[data-key]');
	for (var i=0; i<rows.length; i++) {
		var row = $(rows[i]);
		if (k.indexOf(row.attr('data-key'))==-1) row.remove();
	}
	// remove footer with select if there
	field.find('tfoot').remove();
}

function df_keyvalue_get_values (field) {
	var lines = field.find('[data-key]');
	var data = {};
	var values = {};
	for (var i=0; i<lines.length;i++) {
		var line = $(lines[i])
		var key = line.attr('data-key');
		var input = line.find('input');
		var value = input.val().trim();
		if (value.length>0) values[key] = value;
	}
	data['values'] = values;
	
	return data;
}

function df_keyvalue_edit_mode (field, data) {
	var val = data['values'];
	var k = Object.keys(val);
	k.sort();
	var t = df_keyvalue_get_table(field);
	for (var i=0; i<k.length;i++)
		df_keyvalue_set_pair_rw (t, k[i], val[k[i]]);
	var keys = data['keys'];
	// add footer with select
	df_keyvalue_add_footer (t, keys);
}


/*
 *
 * photo field
 *
 */

function df_photo_create_img_element (field) {
	// find if we already have such an element
	var img = field.find('[data-control=image-display]');
	if (img.length==0) {
		img = document.createElement ('img');
		$(img).addClass('userpic');
		$(img).attr('data-control', 'image-display');
		field.append ($(img));
	} else
		img = img[0]
	return img
}

function df_photo_file_selected (event, field) {
	var element = event.target
	if (element.tagName === 'INPUT') {
		var files = element.files;
		var selectedFile = files[0]
		// the img should be already created
		var img = df_photo_create_img_element (field);
		img.file = selectedFile;
		var reader = new FileReader ();
		reader.onload = (function (aImg) { return function (e) {aImg.src = e.target.result; }})(img);
		reader.readAsDataURL (selectedFile);		
	} else {
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
	var f = $.find('form')[0];
	// find if we have an input element.
	var i = field.find('[type=file]')[0];
	// if not, add it
	if (i===undefined) {
		i = df_photo_create_input (field);		
	}
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
	//console.log (data.url);
	$(img).attr('src', data.url);
	
	// set event on pencil button
	field.find('[data-control=button]').on('click', function (event) {
		var f = field;
		df_photo_select_file(event, f);
	});	
}

function df_photo_get_value (field) {
	var i = field.find('[type=file]')[0];
	if (i === undefined) {
		console.log ('there\'s no input field to find');
		return;
	}
	var files = i.files;
	var data = {};
	if (files.length==1) {
		var file = files[0];
		var fd = new FormData();
		fd.append (field.attr('data-field'), file);
		data['_is_formdata'] = true;
		data['_formdata'] = fd
	}
	return data;
}

function df_photo_handle_error (field, x, s, e) {
	if (x.status == 413) {
		// photo is too large
		alert ('La photo est trop grande, merci de la redimentionner');
		df_set_edit_icon (field);
		df_set_value (field);	
	}
}

function df_photo_initialize (field, data) {
	var f = field.parents('form');
	var i = f.find('[type=file]')[0]
	var img = df_photo_create_img_element (field);
	$(img).attr('src', data.url);
}

/*
 * checkbox control
 */

function df_checkbox_get_checkbox_control (field) {
	c = field.find('[data-control=checkbox]');
	if (c.length==0) {
		c = $('<input type="checkbox" data-control="checkbox">')
		field.append(c)
	}
	return c;
}

function df_checkbox_get_label_control (field, value='') {
	l = field.find('[data-control=label]');
	if (l.length==0) {
		l = $('<span data-control="label">')
		t = l.text(value);
		field.append(l)
	}
	return l;
}

function df_checkbox_change_state (event) {
	field = data_field(event);
	df_save_value (field);
}

function df_checkbox_set_value (field, data) {
	c = df_checkbox_get_checkbox_control (field);
	l = df_checkbox_get_label_control (field, data['label']);
	c.prop('checked', data['value']);
	c.on('change', df_checkbox_change_state);
}

function df_checkbox_get_value (field) {
	c = df_checkbox_get_checkbox_control (field);
	value = c.is(':checked');
	data = { 'value': value };
	return data;
}

/*
 * spécifique a la user-view
 *
 */

$(function(){
	$('[data-field]').each(df_initialize);
});
