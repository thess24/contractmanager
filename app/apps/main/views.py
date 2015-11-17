from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def test(request):
	context= {}
	return render(request, 'main/test.html', context)

def index(request):
	context= {}
	return render(request, 'main/index.html', context)

def user(request):
	context= {}
	return render(request, 'main/user.html', context)

def groups(request):
	context= {}
	return render(request, 'main/groups.html', context)

def group(request, groupname):
	context= {}
	return render(request, 'main/group.html', context)

def newcontract(request):
	context= {}
	return render(request, 'main/newcontract.html', context)

def allcontracts(request):
	context= {}
	return render(request, 'main/allcontracts.html', context)

def analyzecontracts(request):
	context= {}
	return render(request, 'main/analyzecontracts.html', context)

def contractsexpiration(request):
	context= {}
	return render(request, 'main/contractsexpiration.html', context)

def contractsprogress(request):
	context= {}
	return render(request, 'main/contractsprogress.html', context)

def diffcontracts(request, contractid1, contractid2):
	context= {'contractid1':contractid1, 'contractid2': contractid2}
	return render(request, 'main/diffcontracts.html', context)

def editcontract(request, contractid):
	context= {}
	return render(request, 'main/editcontract.html', context)

def contract(request, contractid):
	context= {}
	return render(request, 'main/contract.html', context)

def addtemplate(request):
	context= {}
	return render(request, 'main/addtemplate.html', context)