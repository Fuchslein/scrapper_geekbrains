from scrapper2 import Parser
from pprint import pprint

print("Start HeadHunter")
url = "https://hh.ru"
params = {'text':'python'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 OPR/77.0.4054.90',
'Accept':'*/*'}
data = []

parser = Parser()
search_block={'tag':'div', 'attr':'class', 'value':'vacancy-serp-wrapper'}
block = parser.parse_page(url=url+'/search/vacancy', user_filters=params, user_headers=headers, search_params=search_block)

search_list_block = {'tag':'div', 'attr':'class', 'value':'vacancy-serp'}
block_list=parser.parse_block(block, search_list_block)

search_list ={'tag':'div', 'attr':'class', 'value':'vacancy-serp-item'}
current_job_list = parser.get_list(block=block_list, search_params=search_list)


search_page = {'tag':'a','attr':'data-qa', 'value':'pager-next'}
next_page = parser.get_nextpage_link(url=url, block=block, search_params=search_page)

search_params={
    'vacation':{
        'tag':'a',
        'class':'class',
        'value':'bloko-link'
    },
    'salary':{
        'tag':'span',
        'class':'data-qa',
        'value':'vacancy-serp__vacancy-compensation'
    },
    'link':{
        'tag':'a',
        'class':'data-qa',
        'value':'vacancy-serp__vacancy-title'
    },
    'employer':{
        'tag':'a',
        'class':'data-qa',
        'value':'vacancy-serp__vacancy-employer'
    },
    'location':{
        'tag':'span',
        'class':'data-qa',
        'value':'vacancy-serp__vacancy-address'
    },
    'salary_splitters':{
        'between':'–',
        'min':'от',
        'max':'до'
    }
}
jobs = parser.parse_list(lists = current_job_list, search_params=search_params, url=url)
data+=jobs

while next_page!="null":
    block = parser.parse_page(url=next_page, user_filters=params, user_headers=headers, search_params=search_block)
    block_list=parser.parse_block(block, search_list_block)
    current_job_list = parser.get_list(block=block_list, search_params=search_list)
    jobs = parser.parse_list(lists = current_job_list, search_params=search_params, url=url)
    data+=jobs
    next_page = parser.get_nextpage_link(url=url, block=block, search_params=search_page)


print(len(data))
parser.save_as_json(data,"jobs2")