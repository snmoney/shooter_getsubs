#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017 <snmoney@gmail.com>
import sys
import os
import urllib
import mod_shooter

#init
markFile = "subsscaned.mark";

#1. 接收参数 路径
len_argv = len(sys.argv)
if len_argv<2:
    print("缺少参数path")
    sys.exit()
    
targetPath = sys.argv[1]

#2. 扫描路径 确认目标文件
try:
    filelist = os.listdir(targetPath)
    #print(filelist)
except Exception as e:
    print(e)
    sys.exit()

#2.1 判断路径是否已经处理过
if os.path.exists(targetPath+"/"+markFile):
    sys.exit("这个目录已经处理过");

target = mod_shooter.seekTarget(targetPath)
#print(target)
if target is None:
    mod_shooter.setMark(targetPath, markFile)
    sys.exit("没有需要处理的目标")

#3. 获取目标文件的特征数据
sHash = mod_shooter.shooterHash(target[0])

#4. 调用api 获得字幕文件清单
data_json = mod_shooter.getSubsJSON(target, sHash)
# 备注：我认为有必要保存这个接口返回的列表数据，因为包含delay值，至少在字幕出现位移解决前应该保留
#print(data_json)
links = mod_shooter.parseFromResult(data_json.decode()) #bytes to string
#print(links) #debug ok

#5. 下载字幕文件->命名
if len(links)>0:
    for link in links:
        #mod_shooter.downloadsub(link)
        rfname = mod_shooter.getremotefilename(link) #远端文件名称
        #确定字幕文件的名称
        if os.path.exists(targetPath+"/"+rfname):
            i = 1            
            while os.path.exists(targetPath+"/"+os.path.splitext(rfname)[0]+"."+str(i)+os.path.splitext(rfname)[1]):
                i += 1
            rfname = os.path.splitext(rfname)[0]+"."+str(i)+os.path.splitext(rfname)[1] #修正成不重复的名称
            
        #开始下载
        #subcontent = mod_shooter.downloadsub(link)
        #subfile  = open(targetPath+"/"+rfname, 'w') 
        #subfile.write(subcontent) 
        #以上方法被弃用，由于目标文件的编码方式不确定性增加了下载时对content encode/decode 的复杂性，还不如索性用以下的内建方法下载
        urllib.request.urlretrieve(link, targetPath+"/"+rfname)
    #subfile.close()

#6. 标记已经处理过的目录
mod_shooter.setMark(targetPath)
