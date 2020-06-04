def short_text(text):
    #print(text)
    
    text=text[:len(text)-(len(text)-90)-5]
    text+='[...]'
    return text
        
    


text='Коронавирус: последние новости 4 июня. В COVID нашли инородное тело, Путин отчитал спекулянтов, россиянин открыл стрельбу на просьбу надеть маску'
print(short_text(text))
