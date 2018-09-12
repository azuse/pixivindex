#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import json
import requests
from bs4 import BeautifulSoup
import re
import os
import os.path
import pymysql
import time
import datetime

def imageSearch(files):
    url = "http://www.iqdb.org/"
    proxies = {"http": "socks5://127.0.0.1:1080",
        "https": "socks5://127.0.0.1:1080"}

    # file = requests.get(fileurl)
    data = {
        'service[]':1,
        'service[]':3,
        'service[]':5
        }
    try:
        r = requests.post(url, files=files,data=data, proxies=proxies)
    except requests.exceptions.ProxyError as e:
        print(str(e))
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError ')
        print(str(e))
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError')
        print(str(e))
    except requests.exceptions.HTTPError as e:
        print(str(e))
    except requests.exceptions.Timeout as e:
        print(str(e))

    html = BeautifulSoup(r.text, "html.parser")
    if(html.find(text="No relevant matches")):
        result={"state":-1}
        return result
    picpageURL = html.find(text="Best match").parent.parent.parent.select(
        'td.image')[0].select('a')[0]['href']
    
    similarity = html.find(text=re.compile(".*similarity"))
    try:
        if(picpageURL == None):
            print("not found")
        elif("danbooru" in picpageURL):
            ############################
            # picURL     图片链接
            # sourceURL  图片出处链接
            # author     作者
            # character  人物(未知:None)
            # tags       所有标签
            #############################
            danbooruTEXT = requests.get("https:"+picpageURL, proxies=proxies)
            danbooruHTML = BeautifulSoup(danbooruTEXT.text, "html.parser")

            picURL = danbooruHTML.select("img#image")[0]['src']
            sourceURL = danbooruHTML.select(
                '#post-information')[0].find(text=re.compile("Source.*")).parent.select('a')[0]['href']
            author = danbooruHTML.find('a', itemprop="author").text

            tags = []
            tagsHTML = danbooruHTML.select('.category-0')
            for tagHTML in tagsHTML:
                tag = tagHTML.select('a')[1].text
                tags.append(tag)

            if(danbooruHTML.select(".category-4")):
                character = danbooruHTML.select(
                    ".category-4")[0].select('a')[1].text
            else:
                character = None

        elif("yande.re" in picpageURL):
            ############################
            # picURL     图片链接
            # sourceURL  图片出处链接
            # author     作者
            # character  人物
            # tags       所有标签
            #############################
            yandereTEXT = requests.get(picpageURL, proxies=proxies)
            yandereHTML = BeautifulSoup(yandereTEXT.text, "html.parser")

            picURL = yandereHTML.select("img#image")[0]['src']
            sourceURL = yandereHTML.select('#stats')[0].find(
                text=re.compile("Source.*")).parent.select('a')[0]['href']
            author = yandereHTML.select(
                'li.tag-type-artist')[0].select('a')[1].text

            tags = []
            tagsHTML = yandereHTML.select(".tag-type-general")
            for tagHTML in tagsHTML:
                tag = tagHTML.select('a')[0].text
                tags.append(tag)

            if(yandereHTML.select('.tag-type-character')):
                character = yandereHTML.select(
                    '.tag-type-character')[0].select('a')[1].text
            else:
                character = None

        elif("sankaku" in picpageURL):
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
            if("http" not in picpageURL):
                sankakuTEXT = requests.get("https:"+picpageURL, proxies=proxies, headers=headers)
            else:
                sankakuTEXT = requests.get(picpageURL, proxies=proxies)

            sankakuHTML = BeautifulSoup(sankakuTEXT.text, "html.parser")

            picURL = sankakuHTML.select("img#image")[0]['src']
            sourceURL = ""
            author = sankakuHTML.select(
                ".tag-type-artist")[0].select('a')[0].text

            tags = []
            tagsHTML = sankakuHTML.select(".tag-type-general")
            for tagHTML in tagsHTML:
                tag = tagHTML.select('a')[0].text
                tags.append(tag)

            if(sankakuHTML.select('.tag-type-character')):
                character = sankakuHTML.select(".tag-type-character")[0].select('a')[0].text
            else:
                character = None
        result = {
            'state': 1,
            'picpageURL': picpageURL,
            "picURL": picURL,
            "author": author,
            "similarity": similarity,
            "character": character,
            "tags": tags,
            "sourceURL": sourceURL
        }
    except:
        result = {
            'state': 0,
            'picpageURL': picpageURL,
            "sourceURL": picpageURL,
            'origin': html.text
        }

    return result


rootdir = "e:\pixiv"                                   # 指明被遍历的文件夹
db = pymysql.connect("localhost", "root", "misakaxindex", "pixiv")
cursor = db.cursor()
log = open("picindex.log",'wb')
# 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:  # 输出文件信息
        
        ctime = os.stat(os.path.join(parent, filename)).st_ctime
        createtime = datetime.datetime.fromtimestamp(ctime)

        try:
            sql = """SELECT * FROM `picindex` WHERE `filename` LIKE '%{0}%'""".format(filename)
            # 执行sql语句
            cursor.execute(sql)
            if(cursor._rows != ()):
                print(filename + " skip")
                continue

            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        files = {'file': open(os.path.join(
            parent, filename), 'rb')}  # 输出文件路径信息
        try:
            result = imageSearch(files)
            if(result['state'] == 1):
                tagtext = ""
                for tag in result['tags']:
                    tagtext += tag + ","
                sql = """INSERT INTO picindex(state,
                filename, tag, sourceurl, author, picpageurl,`character`, createtime)
                VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format("tagged", filename, tagtext, result["sourceURL"], result['author'], result['picpageURL'], result['character'],createtime)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # 如果发生错误则回滚
                    db.rollback()
                print(filename + " success")
            elif(result['state'] == -1):
                print(filename + " not found")
                sql = """INSERT INTO picindex(state, filename, tag, sourceurl, author, picpageurl, `character`,createtime) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format("notfound", filename,"","","","","",createtime)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # 如果发生错误则回滚
                    db.rollback()


            else:
                print(filename + " parse error")
                print(result['picpageURL'])
                log.write(filename)
                log.write(result['picpageURL'])
                log.write(result["origin"])
        except BaseException as err:
            print(filename + " failed")
            print(err.args)
            sql = """INSERT INTO picindex(state, filename, tag, sourceurl, author, picpageurl, `character`,createtime) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format("error", filename,"","","","","",createtime)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()
        time.sleep(5)


