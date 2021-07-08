from re import search
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

# https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all
url = 'https://www.kinopoisk.ru'
my_params ={'quick_filters':'serials', 'tab':'all'}
my_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 OPR/77.0.4054.90',
'Accept':'*/*'
}

responce = requests.get(url+'/popular/films/', params=my_params, headers=my_headers)

soup = bs(responce.text, 'html.parser')

searials_block = soup.find('div', {'class':'selection-list'})
serials_list = searials_block.find_all('div', {'class':'desktop-rating-selection-film-item__upper-wrapper'})

serials=[]
for serial in serials_list:
    serial_data={}
    serial_info = serial.find('p')
    serial_name_ru=serial.find('p', {'class':'selection-film-item-meta__name'}).text
    serial_name_en_line=serial.find('p', {'class':'selection-film-item-meta__original-name'}).text
    if ',' in serial_name_en_line:
        serial_name_en_arr = serial_name_en_line.split(',')
        if len(serial_name_en_arr) ==2:
            serial_name_en=serial_name_en_arr[0]
            serial_year=serial_name_en_arr[1]
        elif len(serial_name_en_arr)>2:
            serial_name_en=serial_name_en_arr[0]+', '+serial_name_en_arr[1]
            serial_year=serial_name_en_arr[2]
        else:
            serial_year="n/a"
    else:
        serial_name_en="n/a"
        serial_year=serial_name_en_line
    serial_link =url+serial_info.parent['href']
    serial_additional_block = serial.find('p',{'class':'selection-film-item-meta__meta-additional'})
    serial_origin=serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).text
    serial_theme=serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).next_sibling.text
    serial_rating = serial.find('span', {'class':'rating__value'}).text
    try:
        serial_rating = float(serial_rating)
    except:
        serial_rating=0.0
    serial_data['name']=serial_name_ru
    serial_data['en_name']=serial_name_en
    serial_data['link']=serial_link
    serial_data['origin']=serial_origin
    serial_data['genre']=serial_theme
    serial_data['year']=serial_year
    serial_data['rating']=serial_rating
    serials.append(serial_data)

pprint(serials)
