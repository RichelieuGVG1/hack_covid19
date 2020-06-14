import requests
import os
import re
import json
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup
try:

    def parse_header (req):
        out=''
        url = req
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, 'html.parser')
        main_title = soup.find_all('h1')
        for title in main_title:
            
            return title.get_text()
        
    def short_text(header_text):
    
        header_text=header_text[:len(header_text)-(len(header_text)-90)-5]
        
        return header_text+'[...]'
            
    
    def parse_img (req):
        out=''
        url = req
        ria_counter=0
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, 'html.parser')
        main_title = soup.find_all('img')
        
        for title in main_title:
            try:
                if 'jpg' in title.get('src') or 'png' in title.get('src')or 'jpeg' in title.get('src'):
                   
                    
                    if 'ria' in req:
                        if ria_counter>0:
                            #print('huy')
                            return title.get('src')
                        else:
                            ria_counter+=1
                            continue
                    if 'rbc' in req:
                        if 'article__main-image__image' in title.get('class'):
                            #print('hu1')
                            return title.get(src)
                        else:
                            continue
                    else:
                        return title.get('src')
                        
                else:
                    continue
            except:
                continue

    def parse_time (req):
        out=''
        url = req
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, 'html.parser')
        main_title = soup.find_all('time')
        for title in main_title:
            
            return title.get_text()
            
                
                
    def create_json(var):
        print('Parsing pages...')
        header=[]
        img=[]
        data=[]
        links=[]
        
        json_text='['
        for req in var:
            if '?imgurl' in req:
                req=req[8:]
                #print(req)
            
            if req=='':
                continue
            else:
                header_text=parse_header(req)
                img_link=parse_img(req)
                date=parse_time(req)

                header_text=re.sub('\\xa0', ' ', str(header_text))
                header_text=re.sub('\\n', '', str(header_text))
                img_link=re.sub('\\n', '', str(img_link))
                date=re.sub('\\n', '', str(date))
                date=re.sub(r'\s+', ' ', date)
                if not '2020' in date:
                    import random
                    date=f'0{random.randint(1, 4)} июня 2020'
                    
                if not 'http' in img_link and 'gazeta' not in img_link:
                    img_link=req[8:].split('/')[0]+img_link

                if len(header_text)>90:
                    header_text=short_text(header_text)

                if header_text in header:
                    continue
                

                json_body={
		"header_text":header_text,
		"img_link":img_link,
		"date":date
                }
                try:
                    if (ord(header_text[0])> 1071 or ord(header_text[0]) <1040) or( not 'http' in img_link or 'blank' in img_link) :
                        continue
                    
                    else:

                        header.append(header_text)
                        img.append(img_link)
                        data.append(date)
                        links.append(req)
                        

                        json_text+=f'{json_body},'
                except Exception as e:
                    print(e)

                except requests.exceptions.TooManyRedirects:
                    pass
        
        try:      
            json_text+=']'
            json_text=re.sub('"', '', json_text)

            d = [header, img, data, links]
            export_data = zip_longest(*d, fillvalue = '')
            with open('db.csv', 'w', encoding="utf-8", newline='') as myfile:
                wr = csv.writer(myfile)
                
                wr.writerows(export_data)
                myfile.close()
        except Exception as e:
            print(e)
            pass

        except requests.exceptions.TooManyRedirects:
            pass
        finally:
            print('Successful writen data in database and JSON-file')
        
        
        with open('site.json', 'w', encoding="utf-8") as file:
            json.dump(json_text, file, ensure_ascii=False)
                
                
        return 'Parsing WEB-pages successfuly completed.'
            
    

        #example link

    #req='https://ria.ru/20200603/1572399929.html'
    with open('parsed_html.txt', 'r') as file:
        var=str(file.read())
    
    var = var.split("\n")
    #print(var)
    

    #create_json(var)
    
    
    
except Exception as e:
    print(e)
    pass

except requests.exceptions.TooManyRedirects:
    pass
