import logging
import requests
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime


try:
    def parse_links (max_page, req):
        page = 1
        print('Searching for links...')
        out=''
        while page <= max_page:
            url = req + str(page)
            source_code = requests.get(url)
            soup = BeautifulSoup(source_code.text, 'html.parser')
            main_title = soup.find_all('a')
            for title in main_title:
                if not 'http' in title.get('href') or 'tag' in title.get('href') or 'google' in title.get('href') or 'wiki' in title.get('href')or 'youtu' in title.get('href')or 'vk' in title.get('href') or 'yandex' in title.get('href'):
                    continue
                else:
                    if '&' in title.get('href'):
                        string=title.get('href').split('&')[0]
                    out+=string[7:]
                    out+="\n"
                
                
            page+=1
        with open('parsed_html.txt', 'w') as file:
            file.write(out)
            file.close()
        return 'Parsing links successfuly completed.'
    
except Exception as e:
    print(e)
    logging.basicConfig(filename="logs/error_log.txt", level=logging.ERROR)
    logging.error(e+f'\n{str(datetime.now())}\n\n')
    #os.system('pause')

logging.basicConfig(filename="logs/log_links.txt", level=logging.INFO)
logging.basicConfig(filename="logs/error_log.txt", level=logging.ERROR)

example="https://www.google.com/search?ei=QbTXXs66L-zirgSIsITYCw&q="

description='Hello! This programm can help you to collect necessary internet news, as you want!\n'
print(description)

words=str(input('Enter request, you want to find>>'))
print('Enter just a 3 minus words, which will not be displayed in request>>')
minus_words_list=[str(input()) for i in range(3)]
minus_words=''

for i in range(len(minus_words_list)):
    minus_words+=f"+-{minus_words_list[i]}"


words=re.sub(' ', '+', words)
print(example+words+minus_words)
req=example+words+minus_words
logging.info('\n\n'+words +'\n'+ str(minus_words)+'\n'+ str(datetime.now())+'\n\n')



print(parse_links(1, req))

try:
    with open('parsed_html.txt', 'r') as file:
        var=str(file.read())
        file.close()
        
    var = var.split("\n")
except Exception as e:
    logging.error(e+f'\n{str(datetime.now())}\n\n')

    
from parser_py import parse_header, parse_img, parse_time, create_json
from preprocess import pre

try:
    print(create_json(var))
except Exception as e:
    logging.error(e+f'\n{str(datetime.now())}\n\n')

try:
    print(pre())
except Exception as e:
    logging.error(e+f'\n{str(datetime.now())}\n\n')




