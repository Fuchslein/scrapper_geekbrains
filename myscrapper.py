from scrapper2 import Parser
from pprint import pprint

data=[]
parser = Parser()

print("Start SuperJob")
url="https://www.superjob.ru"
params = {'keywords':'Python','noGeo':1}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 OPR/77.0.4054.90',
'Accept':'*/*'}

search_block={'tag':'div', 'attr':'class', 'value':'_1Ttd8 _2CsQi'}
block = parser.parse_page(url=url+'/vacancy/search', user_filters=params, user_headers=headers, search_params=search_block)

search_list_block = {'tag':'div', 'attr':'class', 'value':'_1ID8B'}
block_list=parser.parse_block(block, search_list_block)

search_list ={'tag':'div', 'attr':'class', 'value':'jNMYr GPKTZ _1tH7S'}
current_job_list = parser.get_list(block=block_list, search_params=search_list)


search_page = {'tag':'a','attr':'class', 'value':'icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe'}
next_page = parser.get_nextpage_link(url=url, block=block, search_params=search_page)

search_params={
    'vacation':{
        'tag':'a',
        'class':'class',
        'value':'icMQ_ _6AfZ9'
    },
    'salary':{
        'tag':'span',
        'class':'class',
        'value':'_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW'
    },
    'link':{
        'tag':'a',
        'class':'class',
        'value':'icMQ_ _6AfZ9'
    },
    'employer':{
        'tag':'a',
        'class':'class',
        'value':'icMQ_ _205Zx'
    },
    'location':{
        'tag':'span',
        'class':'class',
        'value':'_1h3Zg f-test-text-company-item-location e5P5i _2hCDz _2ZsgW'
    },
    'salary_splitters':{
        'between':'—',
        'min':'от',
        'max':'до'
    }
}

jobs = parser.parse_list(lists = current_job_list, search_params=search_params, url=url)
data+=jobs
print("Start cycle")
while next_page!="null":
    block = parser.parse_page(url=next_page, user_filters=params, user_headers=headers, search_params=search_block)
    try:
        block_list=parser.parse_block(block, search_list_block)
        current_job_list = parser.get_list(block=block_list, search_params=search_list)
        jobs = parser.parse_list(lists = current_job_list, search_params=search_params, url=url)
        data+=jobs
        next_page = parser.get_nextpage_link(url=url, block=block, search_params=search_page)
    except:
        break

print(len(data))
parser.save_as_json(data,"jobs2")