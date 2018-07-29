from django.shortcuts import render
from .parse_school import parse_and_save
from .models import *
from django.db.models import Q

# Create your views here.
def home(request):
    districts = [
        'thiruvananthapuram','kollam','pathanamthitta',
        'alappuzha','kottayam','idukki', 'ernakulam',
        'thrissur', 'palakkad', 'malappuram', 'kozhikode',
        'wayanad', 'kannur', 'kasaragod',
    ]  
    return render(request,'home.html',{'districts':districts})

def parse_a_school(request):
    if request.method=='POST':
        url_id = request.POST.get('url_id','')
        if url_id:
            if not School.objects.filter(url_id=url_id):
                result= parse_and_save(int(url_id))
                if result == 'invalid_url':
                    raise Exception('Invalid School Url')
    return render(request,'parse_school.html')

def school_view(request,code):
    school = School.objects.get(code = code)
    return render(request,'school.html',{'school':school})

def schools(request):
    sub_district = request.GET.get('sub_district','')
    name = request.GET.get('name','')
    query = None
    if name: 
        # filtered by name
        schools = School.objects.filter(name__icontains = name)[:20]
        query = name
    elif sub_district: 
        # filtered by dist
        schools = School.objects.filter(sub_district__iexact = sub_district)
        query = sub_district
    else:
        schools = School.objects.order_by('-created_on')[:10]

    return render(request,'schools.html',{'schools':schools,'q':query})

def sub_districts(request,district):
    from .sub_districts import SUB_DISTRICTS
    return render(request,'sub_districts.html',{'sub_districts':SUB_DISTRICTS[district-1]})