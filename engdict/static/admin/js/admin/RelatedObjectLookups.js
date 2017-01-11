// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.

function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showAdminPopup(triggeringLink, name_regexp) {
    var name = triggeringLink.id.replace(name_regexp, '');
    name = id_to_windowname(name);
    var href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
//    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    var win = window.open(href, name, 'height=400,width=1000,resizable=yes,scrollbars=yes');	
    win.focus();
    return false;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    return showAdminPopup(triggeringLink, /^lookup_/);
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
        //add hebin
        var input = $("#" + name);
        input.trigger("updateEvent",["name","val2"]);
        $("td.field-id>input").trigger("updateEvent",["val1","val2"]);
        //end		
    }
    win.close();
}

function showRelatedObjectPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^(change|add|delete)_/, '');
    name = id_to_windowname(name);
    var href = triggeringLink.href;
    //var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
	var win = window.open(href, name, 'height=400,width=1000,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissAddRelatedObjectPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    var o;
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName == 'SELECT') {
            o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elemName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
        // Trigger a change event to update related links if required.
        django.jQuery(elem).trigger('change');
    } else {
        var toId = name + "_to";
        o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}

function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
    objId = html_unescape(objId);
    newRepr = html_unescape(newRepr);
    var id = windowname_to_id(win.name).replace(/^edit_/, '');
    var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
    var selects = django.jQuery(selectsSelector);
    selects.find('option').each(function() {
        if (this.value == objId) {
            this.innerHTML = newRepr;
            this.value = newId;
        }
    });
    win.close();
};

function dismissDeleteRelatedObjectPopup(win, objId) {
    objId = html_unescape(objId);
    var id = windowname_to_id(win.name).replace(/^delete_/, '');
    var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
    var selects = django.jQuery(selectsSelector);
    selects.find('option').each(function() {
        if (this.value == objId) {
            django.jQuery(this).remove();
        }
    }).trigger('change');
    win.close();
};

function dismissAddAnotherPopupForLinkObj(win,newId, newRepr, array) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.

    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    
    var elem = document.getElementById(name);
//add hebin
    var init_value = elem.value;
//end hebin

    var parent = $("#"+name).parent();
    var next = parent.next();
    
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elemName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
//add hebin - for other elem
                var param_id = '';
                var conn, conn1;
                for(var i=0 ; i<array.length; i+=2){
                    
                    param_id = name;
                    conn = "-";  conn1 = array[i]; conn = conn.concat(conn1)
                    param_id = param_id.replace("-id", conn); //shouble be more flexible, extract the info automaticlly , then we're not restricted to "id"
                    var el= document.getElementById(param_id);
                    if(el){
                        el.value = array[i+1];
                    }
					
                    var reg=new RegExp("brbr","g");
                    next.text(array[i+1].replace(reg,"\r\n<br>"))
                    next = next.next();
                }
                if("" == init_value){
                    modify_a(elem);
                }
//end add
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}


function modify_a(el){

    var str;                    
    var obj_id =el.value;
    if(obj_id != ''){
        var a = $(el).prev("a");
        if(a.length > 0){
            a = a[0];
            var href = a.href;
            href = href.replace("/add/","/"+obj_id+"/");
            a.href = href;
            var img = a.innerHTML;
            img = img.replace("icon_addlink.gif","icon_changelink.gif");
            $(a).html(img);
        }
    }

}

// Kept for backward compatibility
showAddAnotherPopup = showRelatedObjectPopup;
dismissAddAnotherPopup = dismissAddRelatedObjectPopup;
