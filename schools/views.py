from django.shortcuts import render
from .parse_school import parse_and_save
from .models import *
from django.db.models import Q

# Create your views here.
def home(request):
    if request.method=='POST':
        url_id = request.POST.get('url_id','')
        if url_id:
            if not School.objects.filter(url_id=url_id):
                parse_and_save(url_id)
    return render(request,'home.html',{'schools':School.objects.all()})

def school_view(request,code):
    school = School.objects.get(code = code)
    return render(request,'school.html',{'school':school})

def schools(request):
    if request.method=='POST':
        # filter_by = request.POST.get('filter_by','')
        query = request.POST.get('query','')
        if query:
            schools= School.objects.filter(
                Q(district__icontains = query) | 
                Q(edu_district__icontains = query) |
                Q(sub_district__icontains = query))
    else:
        schools = School.objects.all()
    return render(request,'schools.html',{'schools':schools})

