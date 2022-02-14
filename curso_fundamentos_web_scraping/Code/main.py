import requests
import lxml.html as html
import os
import datetime

HOME_URL="https://www.larepublica.co"
XPATH_LINKS="//text-fill/a[contains(@href,'www') and contains(text(),'')]/@href"
XPATH_TITTLE="//title[not(contains(@href,'www')) and contains(text(),'') and not(contains(text(),'\n'))]/text()"
XPATH_SUMMARY="//body//div[contains(@*,'lead')]/p/text()"
XPATH_CONTENT="//body//div[contains(@*,'article-wrapper')]//div/p/text()"


def parsed_link(link,archive):
    try:
        response=requests.get(link)
        if response.status_code==200:
            notice=response.content.decode("utf-8")
            parsed=html.fromstring(notice)
            #print(f"parsed: {notice}")
         
         
            try:
                TITLE=parsed.xpath(XPATH_TITTLE)[0]
                print(f"TITLE: {TITLE}")
                TITLE=TITLE.replace('\"',"")
                SUMMARY=parsed.xpath(XPATH_SUMMARY)[0]
                CONTENT=parsed.xpath(XPATH_CONTENT)

            except IndexError:
                #pruebap rint("---"*70)
                #prueba print("RESPONSE")
                return
        
            with open(f"{archive}/{TITLE}.txt", "w", encoding="utf-8") as txt:
                txt.write(TITLE)
                txt.write("\n\n")
                txt.write(SUMMARY)
                txt.write("\n\n")
                for p in CONTENT:
                    txt.write(p)
                    txt.write("\n")
                
        else:
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)



def parse_home():
    '''
        Realiza la primera comunicacion con la pagina y retorna los links de las noticias.
        Si existe un error de comunicacion retorna su respectivo codigo.
        Tabien crea una carpeta en donde guardar las noticias del dia.
    '''
    try:
        #Realiza la peticiones al url
        response=requests.get(HOME_URL)
        #revisa si la conexion es posible
        if response.status_code==200:
            #captura el html y lo decodifica para caracteres con ñ
            home=response.content.decode("utf-8")
            #captura el html de home y lo combierte en algo para hecerle XPATH
            parsed=html.fromstring(home)
            #aplicamos Xpath al documento
            link_to_notice=parsed.xpath(XPATH_LINKS)
            print("len: ",len(link_to_notice))
        
            #var que contiene la fecha de hoy pero escrito con el formato dado.
            today=datetime.date.today().strftime("%d-%m-%Y")
            #si no existe la carpeta "today" creala.
            if not os.path.isdir(today):
                os.mkdir(today)
            
            #aplica la funcion parse_link a cada link
            #print("parse_link")
            for link in link_to_notice:
                print("---"*70)
                parsed_link(link,today)
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__=="__main__":
    run()