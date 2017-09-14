

function adjust_fieldset_horizontal(sFieldset){
    var fs0 = $(sFieldset + ":eq(0)");
    var fs1 = $(sFieldset + ":eq(1)");
    if(fs0.length > 0 && fs1.length > 0 )
    {            
        fs0.css("width","50%");
        fs1.addClass("FloatRight");  // FloatRight already have with property, why only here take effect
        fs1.css({"width":"50%"});
        //fs1.css("top",fs0.position().top);
        fs1.css("top",20);
        if(fs0.height()<fs1.height()){
            fs0.css("height",fs1.height()+5);
        }

        var module_div_Description_textarea = $(sFieldset+":eq(0)>div.field-Description>div>textarea");
        module_div_Description_textarea.css({'width':'60%','height':'50%'});        
    }
}

function adjust_stackInline_fieldset(){
    var filesets = $("div").children(".inline-related");    
    var set = "div.inline-related";
    $(set).css({"position":"relative", "width":"100%"});
    for(var i=0;i<filesets.length;i++)
    {
        var fss = filesets[i];
        $(fss).css({"position":"relative", "width":"100%"});
        var fsid = fss.id;
        if(fsid != ""){
            var sFieldset = "div#" + fsid + ">fieldset";
            adjust_fieldset_horizontal(sFieldset);
        }
    }
}

function adjust_tabularInline_filedset(form_name){
    var s_module_div = "form#";
    s_module_div=s_module_div.concat(form_name);
    s_module_div=s_module_div.concat("_form>div");
    var module_div = $(s_module_div)
    module_div.css({"position":"relative", "width":"100%"});
    
    var module_div_fs0 = $(s_module_div+">fieldset:eq(0)");
    var module_div_fs1 = $(s_module_div+">fieldset:eq(1)");
    var module_div_fs2 = $(s_module_div+">fieldset:eq(2)"); 

    if(module_div_fs1.length > 0){
        module_div_fs1.css("top",module_div_fs0.position().top);
        module_div_fs0.css("width","50%");
        module_div_fs0.css("min-width","450px");    
        module_div_fs1.css("min-width","450px");        
        module_div_fs1.addClass("FloatRight");
        module_div_fs1.css("min-width","450px");    
        if(module_div_fs2.length >0){
            module_div_fs0.css({"border-bottom":"none","border-right":"none"});
            module_div_fs1.css("border-bottom","none");    
            module_div_fs2.css("border-top","none");
        }
        
//        var module_div_Description = $(s_module_div+">fieldset:eq(0)>div.field-Description");
//        var module_div_Description_textarea = $(s_module_div+">fieldset:eq(0)>div.field-Description>div>textarea");    
//        module_div_Description_textarea.css({'width':'60%','height':'50%'});        
////        module_div_Description.css({'width':'90%','height':'40%', 'position': 'relative'}); 

        var module_div_textarea = $(s_module_div+">fieldset:eq(0)>div>div>textarea");    
        module_div_textarea.css({'width':'60%','height':'50%'});        
            
        var max_height = module_div_fs1.height() > module_div_fs0.height() ? module_div_fs1.height() : module_div_fs0.height();
        module_div_fs0.css("height",max_height+5);
        module_div_fs1.css("height",max_height);
    }

}

function update_relation(str_parent, str_son, init_son_value, arrays_parent_value,arrays_id,arrays_value){
//    var str_parent = "id_area"; 
//    var str_son = "id_country"; //

    //for IE, each variable need defined before use, for Fixfox, it's not mandatory
    
    //parent
    var item = "select#";
    item += str_parent;    
    var parent = $(item);  
    item += " option:selected";
    var parent_value = $(item).text();

    //son
    item = "select#";
    item += str_son;
    var son = $(item);
        
    son.html('');
    var selectedIndex = '';
    var firstIndex = '';

//////////////////////////////////////////
    for(var i=0;i<arrays_id.length;i++){    
        if(true == /msie/.test(navigator.userAgent.toLowerCase()))
        {
            parent_value = parent_value.replace("---------",' ');
        }

//        alert(" arrays_parent_value[i] : | " + arrays_parent_value[i]+"|" );
//        alert(" parent_value : |" + parent_value+"|");
        
        if($.trim(arrays_parent_value[i]) == $.trim(parent_value)){            
            
            var opt = new Option(arrays_value[i], arrays_id[i]);  //this only works for Fixfox
            $(opt).html(arrays_value[i]); //to work in IE8, we need this line
            son.append(opt);       
//            son.append("<option value='" + arrays_id[i] + "'>" + arrays_value[i] + "</option>");  //this is work for both IE8 & HTML

            if('' == firstIndex){
                firstIndex = arrays_id[i];
            }
            if(arrays_value[i] == init_son_value && selectedIndex == ''){
                selectedIndex = arrays_id[i];
            }
        }
    }

    if(selectedIndex != ''){
        son.val(selectedIndex);
    }
    else if(firstIndex != ''){
        son.val(firstIndex);
    }
    

    son.change();
}

