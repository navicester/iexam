$(document).ready(function() {
	//alert("haha");
	$("#toggleshow").click(menugroputoggle);
	$("#toggleshow2").click(menugroputoggle2);
	$("#toggleshow3").click(menugroputoggle3);
	$("#toggleshow4").click(menugroputoggle4);
	$("#toggleshow5").click(menugroputoggle5);
	$("#toggleshow6").click(menugroputoggle6);    
});

function show_hide_list(obj)
{
    if($(obj).is(":hidden"))
        $(obj).show();
    else
        $(obj).hide();
}

function menugroputoggle() {
    show_hide_list(".menushowhide");
}

function menugroputoggle2() {
    show_hide_list(".menushowhide2");}

function menugroputoggle3() {
    show_hide_list(".menushowhide3");}

function menugroputoggle4() {
    show_hide_list(".menushowhide4");}

function menugroputoggle5() {
    show_hide_list(".menushowhide5");}

function menugroputoggle6() {
    show_hide_list(".menushowhide6");}

/*
$("#toggleshow").bind("click", function(){  
    alert("Hello World  bind");  
   });
*/   
