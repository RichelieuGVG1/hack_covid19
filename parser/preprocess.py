import requests
import os
import re
import json
import csv

try:
    def pre():
        print('Building WEB-page...')
        main_text_file=''
        with open('header.txt', 'r') as file:
            main_text_file+=str(file.read())
            file.close()

        with open('db.csv', "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            #print(reader)#row, col
            for row in reader:
                #print(row)
                if row[0]=='' or row[1]=='' or row[2]=='' or row[3]=='':
                    continue
                else:
                    main_text_file+=f"<li>\n<div id='news-block'>\n"
                    main_text_file+=f"<a href='{row[3]}'>\n"
                    main_text_file+=f"<img id='new-img' src='{row[1]}'>\n"
                    main_text_file+=f"<strong>\n<div id='header'>{row[0]}</div>\n</strong>\n"
                    main_text_file+=f"<div id='date'>{row[2]}</div>\n</a></div>\n</li>\n\n"
            
        with open('footer.txt', 'r') as file:
            main_text_file+=str(file.read())
            file.close()
    
        with open('news.html', 'w', encoding="utf-8") as file:
            file.write(main_text_file)
            file.close()
            
        return 'Building WEB-page successfuly completed. Program finished.'
    
except Exception as e:
    print(e)
    
    pass
finally:
    os.system('pause')







