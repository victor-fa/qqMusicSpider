#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib2
import os
import re
from bs4 import BeautifulSoup
import mechanize
import urllib
import traceback
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
getnmID="getUCGI4637003703166609"
page_number = 5
city_name = 'aomen'
max_number = 15
index_number=13  # 1~26 对应 A~Z

temp=sys.stdout

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, " ", title)  # 替换为下划线
    return new_title

for page in range(page_number,max_number+1):

    #sys.stdout = open(city_name+str(page)+'.txt', 'w')
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2;\
                        WOW64) AppleWebKit/537.11 (KHTML, like Gecko)\
                        Chrome/23.0.1271.97 Safari/537.11')]
    #query = "https://"+city_name+".8684.cn/line"+str(page)
    query ="https://u.y.qq.com/cgi-bin/musicu.fcg?callback="+getnmID+"&g_tk=5381&jsonpCallback=getUCGI4637003703166609&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A"+str(index_number)+"%2C%22sin%22%3A"+str((page-1)*80) +"%2C%22cur_page%22%3A"+str(page)+"%7D%7D%7D"

    #query_base = "https://" + city_name + ".8684.cn"
    query_base = "https://y.qq.com/portal/singer_list.html"
    wrong_website_list = []
    current_website = ''
    singer_name=''
    album_json_text=''
    try:

        htmltext = br.open(query).read()
        json_text=htmltext.strip(getnmID+"(").strip(")")


        singer_list_jsonData=json.loads(json_text)
        singer_list=singer_list_jsonData.get("singerList").get("data").get("singerlist")

        folder = "d:\\pachong\\" + 'S'+str(index_number)
        # 获取此py文件路径，在此路径选创建在new_folder文件夹中的test文件夹

        if not os.path.exists(folder):
            os.makedirs(folder)
        for singer_data in singer_list:
            singer_name=singer_data.get("singer_name")
            singer_name=validateTitle(singer_name)
            sys.stdout = open(folder+"\\"+singer_name+".txt", 'w')
            singermid=singer_data.get("singer_mid")
            query_album='https://u.y.qq.com/cgi-bin/musicu.fcg?callback='+getnmID+'&g_tk=5381&jsonpCallback=getUCGI06449673347468199&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"singerAlbum":{"method":"get_singer_album","param":{"singermid":"'+singermid+'","order":"time","begin":0,"num":10000,"exstatus":1},"module":"music.web_singer_info_svr"}}'
            album_text = br.open(query_album).read()
            album_json_text = album_text.strip(getnmID + "(").strip(")")
            album_list_jsonData = json.loads(album_json_text)

            if album_list_jsonData is None \
                    or not album_list_jsonData.has_key('singerAlbum')\
                    or not album_list_jsonData.get("singerAlbum").has_key('data')\
                    or not  album_list_jsonData.get("singerAlbum").get("data").has_key('list'):
                album_text = br.open(query_album).read()
                album_json_text = album_text.strip(getnmID + "(").strip(")")
                album_list_jsonData = json.loads(album_json_text)
                sys.stdout = temp
                print("1-》"+singer_name)
                print(album_list_jsonData)
                sys.stdout = open(folder + "\\" + singer_name + ".txt", 'w')

            if album_list_jsonData is None \
                    or not album_list_jsonData.has_key('singerAlbum') \
                    or not album_list_jsonData.get("singerAlbum").has_key('data') \
                    or not album_list_jsonData.get("singerAlbum").get("data").has_key('list'):
                sys.stdout = temp
                print("2-》" + singer_name)
                print(album_list_jsonData)
                sys.stdout = open(folder + "\\" + singer_name + ".txt", 'w')
                continue

            album_list = album_list_jsonData.get("singerAlbum").get("data").get("list")

            if album_list is None or len(album_list)==0:
                print("\t这个人贼可怜一张专辑都没有")
                continue
            else:
                for album_data in album_list:
                    print ("\t"+album_data.get("album_name"))
                    albummid = album_data.get("album_mid")
                    query_song = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid='+str(albummid)+'&g_tk=5381&jsonpCallback=albuminfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
                    song_text = br.open(query_song).read()
                    song_json_text = song_text.strip(" albuminfoCallback(").strip(")")

                    song_list_jsonData = json.loads(song_json_text)
                    song_list = song_list_jsonData.get("data").get("list")
                    for song_data in song_list:
                            print ("\t\t" + song_data.get("songname")+"\t-"
                                   +song_data.get("singer")[0].get("name"))

        # soup = BeautifulSoup(htmltext, "lxml")
        #
        # # all_links =  soup.find_all('h3',{'class':'r'})   # resource link
        # #all_bus_div = soup.find_all('div', {"id": "con_site_1"})
        # all_a_singer = soup.find_all("a")
        #
        # #print(all_a_singer.__len__())
        # for a in all_a_singer:
        #     link_text = a.text
        #     link_adress = a['href']
        #    # print(link_text).encode('utf-8')+"\t"+link_adress
        #     new_address = query_base + link_adress
        #     current_website = new_address
        #     detailed_html = br.open(new_address).read()
        #     detailed_soup = BeautifulSoup(detailed_html, "lxml")
        #     all_detailed_div_list = detailed_soup.find_all('div', {"class": "bus_line_site"})
        #     print(len(all_detailed_div_list))
        #     for trip in all_detailed_div_list:
        #         for station_div_list in trip.children:
        #             for station_div in station_div_list.children:
        #                 station_text = station_div.a.text
        #                 print(station_text).encode('utf-8')
        #         print('-----返程-----')
    except Exception as e:
        sys.stdout = temp

        print(singer_name)
        print(album_json_text)
        print(repr(e))
        wrong_website_list.append(current_website)
        traceback.print_exc()
        print('there is something wrong with the internet')