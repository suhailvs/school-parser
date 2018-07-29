import requests
from bs4 import BeautifulSoup
from datetime import datetime

def find_codes(soup):    
    codes = []
    for a in soup.find_all('a', href=True):
        url_id = a['href'].rsplit('/')[-1]
        if url_id.isdigit():
            codes.append(url_id)
    return codes    

def get_subdistricts_from_edu(edu):
    sub_dists = []
    url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/edu/'
    r = requests.get('%s%s'%(url,edu))
    soup = BeautifulSoup(r.text, "html.parser") 
    table = soup.select("tr")
    for tr in table:
        tds = tr.findAll('td')
        if len(tds)>1:
            sub_dists.append(tds[1].text.strip())
    return sub_dists

def get_subdistricts(district):
    sub_dists = []  
    get_edus_url = 'http://103.251.43.156/schoolfixation/index.php/Publicview/index/rev/'
    r = requests.get('%s%s'%(get_edus_url,district))
    soup = BeautifulSoup(r.text, "html.parser")
    edu_codes = find_codes(soup) 
    for edu in edu_codes:
        res = get_subdistricts_from_edu(edu)
        sub_dists.extend(res)
    return sub_dists


if __name__=='__main__':    
    sub_dists_dict = []
    for i in range(1,15):
        sub_dists_dict.append(get_subdistricts(i))
    print (sub_dists_dict)
    print ('copy above list to schools/sub_districts.py')
    