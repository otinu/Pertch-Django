from django.shortcuts import render

def testfunc(request):
    return render(request, 'owner/test.html')