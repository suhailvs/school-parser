import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import *

def parse_and_save(url_id = 8478):
    problamatic_urls = [
        21359, # date wrong format
        13059, # invalid url
        11126, # date wrong format employee
        13071, # date wrong format employee
        10559, # date wrong format employee
        8980,# invalid url
    ]
    if url_id in problamatic_urls: return 'problamatic_url'
    # asmmhss = 8478     
    url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/schoolsdetails/'
    r = requests.get('%s%s'%(url,url_id))
    soup = BeautifulSoup(r.text, "html.parser")
    h5_tag = soup.select("h5")
    if not h5_tag: 
        print ('invalid_url: %s%s'%(url,url_id))
        return 'invalid_url'
    tables = soup.select("table")
    to_int = lambda x: 0 if x in ['-',''] else int(x)
    # School code, district etc
    table_data = tables[0].select('tr')[1].findAll('td')
    school,is_created = School.objects.get_or_create(
        url_id = url_id,
        code= table_data[0].text.strip(),
        name= h5_tag[0].text.split(':')[1].strip(),
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
            school_binfo.rooms = to_int(cells[1].text.strip())
        elif 'Total Teaching Staff' in cells[0].text.strip():
            school_binfo.teaching_staffs = to_int(cells[1].text.strip())
        elif 'Non-Teaching Staff' in cells[0].text.strip():
            school_binfo.non_teaching_staffs = to_int(cells[1].text.strip())
    
    school_binfo.save()
    school.basic_info = school_binfo
    school.save()

    # Student Strength
    # print('Student Strength')
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
    # print('Staff Strength')
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


    # print('Employee Details')
    table_data = tables[5].select('tr')
    for i,tr in enumerate(table_data):
        cells = tr.findAll('td')
        if i == 0: continue
        date_join = cells[3].text.strip()
        if date_join == '00-00-0000':
            date_join = datetime.now()
        else: date_join = datetime.strptime(date_join, '%d-%m-%Y')
        school_staffs = Staff(
            school = school, 
            name = cells[1].text.strip(),
            designation = cells[2].text.strip(),
            date_of_join = date_join,
        )
        school_staffs.save()

    print ('Successfully saved: %s' %(url_id))
    return 'success'


def find_codes(url,id):
    r = requests.get('%s%s'%(url,id))
    soup = BeautifulSoup(r.text, "html.parser")
    codes = []
    for a in soup.find_all('a', href=True):
        url_id = a['href'].rsplit('/')[-1]
        if url_id.isdigit():
            codes.append(url_id)
    return codes

def parse_by_subdistrict(sub_district = 212):
    # alathur = 212
    url ='http://103.251.43.156/schoolfixation/index.php/Publicview/index/schools/'
    school_url_ids = find_codes(url,sub_district)
    #print (school_url_ids)
    for url_id in school_url_ids:
        if not School.objects.filter(url_id=url_id):
            parse_and_save(url_id)
        

def parse_by_edudistrict(edu_district = 21):
    # palakkad = 21
    # palakkad_edu district = 212 to 217
    url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/edu/'
    subdistrict_url_ids = find_codes(url,edu_district)
    #print (subdistrict_url_ids)
    for url_id in subdistrict_url_ids:
        parse_by_subdistrict(url_id)

def parse_by_district(district = 9):
    url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/rev/'
    district_url_ids = find_codes(url,district)    
    for url_id in district_url_ids:
        parse_by_edudistrict(url_id)

def parse_all(district=None):
    if district: 
        # trissur = 8, palakkad = 9
        parse_by_district(district)
    else:
        for district in range(1,15):
            parse_by_district(district)