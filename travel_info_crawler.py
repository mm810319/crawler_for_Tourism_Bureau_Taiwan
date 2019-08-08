# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url="https://www.taiwan.net.tw/m1.aspx?sNo=0001016"
response=requests.get("https://www.taiwan.net.tw/m1.aspx?sNo=0001016")
html=BeautifulSoup(response.text)
data=html.find("a",title="觀光景點")
area=html.find_all("a",attrs={"title":re.compile(".*?地區")})
area_url=[]
for i in range( len(area) ):
    print(area[i]["title"],area[i]["href"])
    if i < 5:
        area_url.append({"地區":area[i]["title"],"url":"https://www.taiwan.net.tw/"+area[i]["href"]})
area_info=[]
output_data=[]
for area in area_url:
    url=area["url"]
    response=requests.get(url)
    html_area=BeautifulSoup(response.text)
    #r=html_area.find("div",class_="mapside")
    area_introduction=html_area.find("p").text
    area_info.append({"地區":area["地區"],"簡介":area_introduction})
    print(area["地區"])
    #html.find_all("span",class_="circularbtn-img"")
    city_list=html_area.find("ul",class_="circularbtn-list").find_all("a")
    city_output_list=[]
    for city in city_list:
#        r_temp=city.find("a")
        city_url="https://www.taiwan.net.tw/"+city["href"]
        response_city=requests.get(city_url)
        html_city=BeautifulSoup(response_city.text)        
        city_temp=html_city.find("div",class_="content")
        city_temp=city_temp.find("div",class_="wrap")
        city_name=city_temp.find("h2").text  
        city_introduction=city_temp.find_all("p")
        city_introduction="\n".join([i.text for i in city_introduction])
        print(city_name)
        attraction_list=html_city.find_all("div",class_="card-wrap")
        attr_list=[]
        for attraction in attraction_list:
            
            attr_temp=attraction.find("a")
            attr_url="https://www.taiwan.net.tw/"+attr_temp["href"]
            resposne_attr=requests.get(attr_url)
            html_attr=BeautifulSoup(resposne_attr.text)
            attr_title=html_attr.find("div",class_="title").find("h2").text
            print(attr_title)    
            attr_body=html_attr.find("div",class_="content").find("div",class_="wrap"
                      ).find_all("p")[1].text
            info_title=html_attr.find("dl",class_="info-table").find_all("dt")
            
            info=html_attr.find("dl",class_="info-table").find_all("dd")
            attr_dic={"景點":attr_title, "景點簡介":attr_body}
            for i in range( len(info_title)):                
                info_title[i]=info_title[i].text           
                info_title[i]=info_title[i].replace("/","").replace("：","")
                if info_title[i]=="網站":
                    info_dic={info_title[i]:info[i].find("a")["href"]}
                else:
                    info_dic={info_title[i]:info[i].text}
                attr_dic.update(info_dic)
                

            attr_list.append(attr_dic)
        city_dict={"縣市名稱":city_name,
                    "縣市簡介":city_introduction,
                    "觀光景點資訊":attr_list}   
        city_output_list.append(city_dict)
    area_dict={"地區":area["地區"],"地區簡介":area_introduction,"縣市資訊":city_output_list}
    output_data.append(area_dict)
with open("travel_info.json", 'w',encoding="utf-8") as outfile:
    outfile.write(json.dumps(output_data,ensure_ascii= False,indent=4, sort_keys=True))
outfile.close()
