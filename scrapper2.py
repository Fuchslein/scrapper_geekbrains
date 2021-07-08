import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from urllib.parse import urlparse
import json
import csv

class Parser():
    """Handmade parser for webpages
    """
    def __init__(self):
        super().__init__()
        self.counter = 0


    def parse_page(self, url, user_filters, user_headers, search_params):
        responce = requests.get(url, params=user_filters, headers=user_headers)
        soup = bs(responce.text, 'html.parser')
        block=soup.find(search_params['tag'],{search_params['attr']:search_params['value']})
        return block


    def parse_block(self, block, search_params):
        return block.find(search_params['tag'],{search_params['attr']:search_params['value']})


    def get_list(self, block, search_params):
        return block.find_all(search_params['tag'], {search_params['attr']:search_params['value']})


    def get_nextpage_link(self, url ,block, search_params):
        try:
            next_req = block.find(search_params['tag'], {search_params['attr']:search_params['value']})['href']
        except:
            next_req = "null"
        if next_req!="null":
            return url + next_req
        else:
            return "null"


    def parse_list(self, lists, search_params, url):
        jobs=[]
        for line in lists:
            try:
                jobs.append(self.parse_item(line=line, search_params=search_params, url=url))
            except:
                continue
        return jobs


    def parse_item(self, line, search_params, url):
        data={}
        vacation_name=line.find(search_params['vacation']['tag'], {search_params['vacation']['class']:search_params['vacation']['value']}).text
        try:
            salary_line=line.find(search_params['salary']['tag'], {search_params['salary']['class']:search_params['salary']['value']}).text
            salary_line = salary_line.lower()
            salary_line= salary_line.replace(" ","").replace('\u202f','')
            salary_line=salary_line.replace('.','')
            salary = salary_line[:-3]
            currency=salary_line[-3:]
            salary_min=0
            salary_max=0
            if search_params['salary_splitters']['between'] in salary:
                arr = salary.split('–')
                salary_min=arr[0]
                salary_max=arr[1]
            elif search_params['salary_splitters']['min'] in salary:
                salary_min=salary[2:]
            elif search_params['salary_splitters']['max'] in salary:
                salary_max=salary[2:]
            else:
                salary_min=0
                salary_max=0
        except:
            salary_min=0
            salary_max=0
            currency=''
        vacation_url=line.find(search_params['link']['tag'], {search_params['link']['class']:search_params['link']['value']})['href'].split('?')[0]
        parsed_uri = urlparse(url)
        hunter_url='{uri.netloc}'.format(uri=parsed_uri)
        try:
            employer=line.find(search_params['employer']['tag'], {search_params['employer']['class']:search_params['employer']['value']}).text
        except:
            employer=""
        try:
            location=line.find(search_params['location']['tag'], {search_params['location']['class']:search_params['location']['value']}).text
        except:
            location=""

        data['vacation_name']=vacation_name
        data['salary_min']=salary_min
        data['salary_max']=salary_max
        data['currency']=currency
        data['hunter']=hunter_url
        data['employer']=employer
        data['location']=location
        data['vacation_url']=vacation_url
        return data


    def save_as_json(self, data, filename):
        out_file=open(filename+".json", "w", encoding='utf-8')
        json.dump(data, out_file, indent=6, ensure_ascii=False)
        out_file.close()


    def save_as_csv(self, data, filename):
        fields = ['Vacation_Name', 'Salary_Min', 'Salary_Max', 'Currency', 'Hunter', 'Employer', 'Location', 'URL']
        csv_file = filename + ".csv";
        with open(csv_file,'w') as csvfile:
            csvwriter=csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(data.values())
