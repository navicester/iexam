
//document.write("<script language='javascript' src='/static/admin/js/admin/RelatedObjectLookups.js'></script>");
//document.write("<script language='javascript' src='/static/admin/js/jquery.init.both.js'></script>");


//Use ajax to retrieve data later

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
        //add hebin
        //var input = $("#" + name);
        //input.trigger("updateEvent",["name","val2"]);
        //$("td.field-id>input").trigger("updateEvent",["val1","val2"]);
        //end		
    }
    win.close();
}



//add hebinn
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

//    var parent = $("#"+name).parent();
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
					
                    // var reg=new RegExp("brbr","g");
                    // next.text(array[i+1].replace(reg,"\r\n<br>"))
                    var reg=new RegExp("brbr","g");
                    next.text(array[i+1].replace(reg,"\r\n"))                    
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
//end add
