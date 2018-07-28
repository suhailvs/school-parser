import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import *


def parse_and_save(url_id):    
    url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/schoolsdetails/'
    r = requests.get('%s%s'%(url,url_id))
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.select("table")
    to_int = lambda x: 0 if x=='-' else int(x)
    # School code, district etc
    table_data = tables[0].select('tr')[1].findAll('td')
    school,is_created = School.objects.get_or_create(
        url_id = url_id,
        code= table_data[0].text.strip(),
        name= soup.select("h5")[0].text.split(':')[1].strip(),
        district= table_data[1].text.strip(),
        edu_district= table_data[2].text.strip(),
        sub_district= table_data[3].text.strip())

    
    # School Basic Info
    table_data = tables[1].select('tr')
    school_binfo = school.basic_info #BasicInfo()
    if not school_binfo: school_binfo = BasicInfo()

    for tr in table_data:
        cells = tr.findAll('td')
        if 'Establishment' in cells[0].text.strip():
            school_binfo.establish_date = cells[1].text.strip()
        elif 'Area' in cells[0].text.strip():
            school_binfo.area = cells[1].text.strip()
        elif 'Rooms' in cells[0].text.strip():
            school_binfo.rooms = cells[1].text.strip()
        elif 'Total Teaching Staff' in cells[0].text.strip():
            school_binfo.teaching_staffs = cells[1].text.strip()
        elif 'Non-Teaching Staff' in cells[0].text.strip():
            school_binfo.non_teaching_staffs = cells[1].text.strip()
    
    school_binfo.save()
    school.basic_info = school_binfo
    school.save()

    # Student Strength
    print('Student Strength')
    table_data = tables[2].select('tr')
    for i,tr in enumerate(table_data):
        cells = tr.findAll('td')
        course = cells[0].text.strip()
        if i == 0 or course == 'Total': continue

        school_students = StudentStrength(
            school = school, 
            course=  to_int(cells[0].text.strip()),
            strength= to_int(cells[1].text.strip()),
            sampoorna = to_int(cells[2].text.strip()),
            available_uid = to_int(cells[3].text.strip()),
            valid_uid = to_int(cells[4].text.strip()),
            partialy_match_uid = to_int(cells[5].text.strip()),
            invalid_uid = to_int(cells[6].text.strip()),
            none  = to_int(cells[7].text.strip()),
            )
        school_students.save()


    # staff strength 2014-15, 2010-11
    print('Staff Strength')
    table_data = tables[3].select('tr')
    for i,tr in enumerate(table_data):
        cells = tr.findAll('td')
        course = cells[0].text.strip()
        if i == 0 or course == 'Total': continue
        school_staff_strength = StaffStrength(
            school = school, 
            year= '2015',
            designation=cells[0].text.strip(),
            strength = to_int(cells[1].text.strip())
            )
        school_staff_strength.save()
    
    table_data = tables[4].select('tr')
    for i,tr in enumerate(table_data):
        cells = tr.findAll('td')
        course = cells[0].text.strip()
        if i == 0 or course == 'Total': continue
        school_staff_strength = StaffStrength(
            school = school, 
            year= '2011',
            designation=cells[0].text.strip(),
            strength = to_int(cells[1].text.strip())
            )
        school_staff_strength.save()


    print('Employee Details')
    table_data = tables[5].select('tr')
    for i,tr in enumerate(table_data):
        cells = tr.findAll('td')
        if i == 0: continue
        school_staffs = Staff(
            school = school, 
            name = cells[1].text.strip(),
            designation = cells[2].text.strip(),
            date_of_join = datetime.strptime(cells[3].text.strip(), '%d-%m-%Y'),
        )
        school_staffs.save()