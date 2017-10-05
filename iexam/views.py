from django.shortcuts import render

def about(request):
	return render(request, "about.html", {})

def test(request):
	return render(request, "admin/linked/linkback.html", {})	
