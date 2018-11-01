#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import lxml.html
import requests
import re
import os
from os import path
import glob
import shutil
import subprocess
#import shlex
#from ftplib import FTP
from logging import getLogger,StreamHandler,DEBUG
from datetime import datetime
import sys
import configparser
import distutils.util

from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter

#variables

#methods
def make_logger():
    try:
        #logファイル作成 https://qiita.com/amedama/items/b856b2f30c2f38665701、https://qiita.com/HirotakaK/items/d8b4ddbd953e15a43492
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        # フォーマッタを生成する
        fmt = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #標準出力用ハンドラーを生成する
        stream_handler = StreamHandler()
        stream_handler.setLevel(DEBUG)
        # ハンドラーにフォーマッターを設定する
        stream_handler.setFormatter(fmt)
        logger.addHandler(stream_handler)

        # ファイル出力ハンドラーを生成する
        # 現在日付
        todayYYYYMMDD = datetime.today().strftime("%Y%m%d")
        logDirectory = os.path.dirname(os.path.abspath(__file__))
        fileHandler = FileHandler(logDirectory.replace(os.path.sep, '/') + '/' + todayYYYYMMDD + '.log')
        fileHandler.setFormatter(fmt)

        # ロガーにハンドラーを設定する
        logger.addHandler(fileHandler)
        return logger
    except Exception as e:
        logger.error('Traceback',stack_info = True)
        logger.error(e)

def get_today_JPGFile_name():
    print('JPGFileName is JPG_20180XX')
    i = input("Please input today's Number (20180XX)")
    return i

def confirm_file_name(arg_filename):
    print('Is it OK todayJPGFileName is ' + arg_filename + '?')
    input_confirm_todayJPGFileName = input('（y/n）>>')
    print(input_confirm_todayJPGFileName+'input(">>")')
    if(input_confirm_todayJPGFileName[0] == 'y'):
        return True
    else:
        return False

def main():
    try:

        logger = make_logger()
        
         #config.iniの読み込み----------------------------------------------------------------------------------------start
        inifile = configparser.ConfigParser()
        inifile.read('./config.ini','UTF-8')

        todayJPGFileName = inifile.get('targetfile', 'todayJPGFileName')
        todayJPHFileName = todayJPGFileName.replace("JPG","JPH")#JPH_
        #isDownloadJPG = bool( distutils.util.strtobool( inifile.get('settings', 'isDownloadJPG') ) )
        #isDownloadJPH = bool( distutils.util.strtobool( inifile.get('settings', 'isDownloadJPH') ) )
        #isDoCopy = bool( distutils.util.strtobool(inifile.get('settings', 'isDoCopy')))
        myDowmloadDir = inifile.get('settings', 'myDowmloadDir')
        myJPGWorkDir = inifile.get('settings', 'myJPGWorkDir')
        myJPHWorkDir = inifile.get('settings', 'myJPHWorkDir')
        #download_span = int(inifile.get('settings', 'download_span'))
        
        #config.iniの読み込み----------------------------------------------------------------------------------------end

        #★confirm_file_name()
        try:

            #subprocess.call('cd /d {}'.format(myJPGWorkDir), shell=True)
            res = subprocess.check_call('ls')
            print(res)
        except:
            print('Error.')

        #解凍処理
        #中途半端にしかできない　容量制限？
        # cmdbash = "bash"
        # subprocess.Popen(cmdbash,cwd=myJPGWorkDir,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        cmdjpgtar = "bash -c \'tar xvfz {}.tar.gz -C {}\';".format(todayJPGFileName,todayJPGFileName)
        #cmdjpgtarbash = ''+cmdjpgtar+''
        process3 = subprocess.Popen(cmdjpgtar,cwd=myJPGWorkDir,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        #subprocess.Popen(cmdbash,cwd=myJPHWorkDir,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        cmdjphtar = "bash -c \'tar xvfz " + todayJPHFileName + ".tar.gz -C " + todayJPHFileName +"\';"
        #cmdjphtarbash = ''+cmdjpgtar+''
        process4 = subprocess.Popen(cmdjphtar,cwd=myJPHWorkDir,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        process3.wait()
        process4.wait()


    except Exception as e:
        if logger is not None:
            logger.error('Traceback',stack_info = True)
            logger.error(e)

if __name__ == '__main__':
    main()

        
