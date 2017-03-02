#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017 <snmoney@gmail.com>
import os
import math
import hashlib
import json
import urllib, urllib.parse, urllib.request

#查找路径下的目标文件（不适用于遍历处理多个文件的字幕下载）
#返回 [FilePath,FileSize] 或 None
def seekTarget(path):
    mediaTypes = [".mp4", ".avi", ".wmv",".mkv",".mpeg"]
    
    
    if os.path.exists(path):
        if os.path.isdir(path):
            flist = os.listdir(path)
            maxSizeFile = ""
            maxSize = 0
            for fname in flist:    
                #只处理目标文件
                if (os.path.isfile(path+"/"+fname)) and (os.path.splitext(fname)[1] in mediaTypes) : 
                    curSize = os.path.getsize(path+"/"+fname)
                    if curSize>maxSize:
                        maxSize = curSize
                        maxSizeFile = path+"/"+fname            
    #else: #skip
            if maxSize==0:
                #sys.exit("没有可操作的目标文件")
                return None
            return [maxSizeFile, maxSize] #目标值    
        else: 
            #是文件
            if os.path.splitext(path)[1] in mediaTypes:
                return path 
            else:
                return None
            
    else:
        return None
        #sys.exit("目标路径不存在")
    
#射手接口要求的hash算法    
def shooterHash(fpath):
    if len(fpath)==0: 
        return None    
    
    fp = open(fpath,'rb')
    fsize = os.path.getsize(fpath)
    #print 'file size :',fsize
    
    pos1 = 4096
    pos2 = int(math.floor(fsize/3)) #python3 中 int 与long 整合，不再区分
    #print "type: %s; value: %s" %(type(pos2),pos2) #debug
    pos3 = int(math.floor(fsize*2/3))
    pos4 = int(fsize - 8192)
    bsize = 4096
    
    fp.seek(pos1)
    raw = fp.read(bsize)
    key1 = hashlib.md5(raw).hexdigest()
    
    fp.seek(pos2)
    raw = fp.read(bsize)
    key2 = hashlib.md5(raw).hexdigest()
    
    fp.seek(pos3)
    raw = fp.read(bsize)
    key3 = hashlib.md5(raw).hexdigest()
    
    fp.seek(pos4)
    raw = fp.read(bsize)
    key4 = hashlib.md5(raw).hexdigest()
    
    fp.close()
    
    #output
    #print "%s;%s;%s;%s" %(key1,key2,key3,key4)
    return "%s;%s;%s;%s" %(key1,key2,key3,key4)

def getSubsJSON(path, hash):
    params = {"filehash":hash, "pathinfo":path, "format":"json", "lang":"chn"}
    post_data = urllib.parse.urlencode(params)
    post_data=post_data.encode(encoding='UTF8') #解决报警 说post data只能是bytes 不能是str的错误
    requrl = "https://www.shooter.cn/api/subapi.php"
    req = urllib.request.Request(requrl,post_data)
    res_data = urllib.request.urlopen(req)
    res = res_data.read()
    #print(res)
    return res

#目标应该将json拆解成下载地址返回
def parseFromResult(str_json):
    links = [] #init
    
    for sfile in json.loads(str_json):
        #print(sfile["Files"])
        links.append(sfile["Files"][0]["Link"])

    #exit() #debug break
    return links


def downloadsub(link):
    #rfname = getremotefilename(link)    
    response = urllib.request.urlopen(link)
    content = response.read()
    
    #print(content)
    print("downloading:"+link)
    #exit() 
    return content.decode('utf-8', 'ignore') #返回str 不返回bytes

#获取远端文件的文件名，从header提取
def getremotefilename(link):
    req = urllib.request.Request(link, method='HEAD')
    r = urllib.request.urlopen(req)
    #print(r.info().get_filename())
    return r.info().get_filename()

def test():
    print("ok")

