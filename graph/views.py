from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    #this is the shape of the request add your logic here based on that.
    print(request.POST.dict()['json'])
    return render(request, 'index.html')
