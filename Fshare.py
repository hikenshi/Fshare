from lib2to3.pgen2.tokenize import TokenError
import subprocess
import json
import logging
import sys
from sys import exit
import inspect
import re
import os

def run_and_printchar(args):
    #credit to https://gist.github.com/autosquid/6acb386b5d5132516c1d6d87081310be about process bar of wget
    try:
        pipe = subprocess.Popen(args, bufsize = 0,
            shell = False,
            stdout = None, # no redirection, child use parent's stdout
            stderr = subprocess.PIPE) # redirection stderr, create a new pipe, from which later we will read
    except Exception as e:
        #inspect.stack()[1][3] will get caller function name
        logging.error(inspect.stack()[1][3] + ' error: ' + str(e))
        return False
    while 1:
        #use read(1), can get wget progress bar like output
        s = pipe.stderr.read(1)
        if s:
            sys.stdout.buffer.write(s)
        if pipe.returncode is None:
            code = pipe.poll()
        else:
            break
    if not 0 == pipe.returncode:
        return False
    return True

def layLinkFolder(url_folder, namefile, token, session_id, useragent):
    CurlUrlFolder = 'curl -X POST "https://api.fshare.vn/api/fileops/getFolderList" -H  "accept: application/json" -H  "User-Agent: %s" -H  "Cookie: session_id=%s" -H  "Content-Type: application/json" -d "{\\"url\\":\\"%s\\",\\"dirOnly\\":0,\\"pageIndex\\":0,\\"limit\\":60,\\"token\\":\\"%s\\"}"' %(useragent, session_id, url_folder, token)
    status2, output2 = subprocess.getstatusoutput(CurlUrlFolder)
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,output2)
    url_ = []
    for i in url:
        for j in i:
                if len(j) < 2:
                    continue
                url_.append('{"link":"'+j.replace("}","").replace("{","")+'"}')

    with open(namefile, "w") as fp:
        for i in url_:
            fp.write(json.loads(i)['link']+' '+json.loads(i)['ftitle']+'\n')
    return True

def login(password, email, useragent, appkey):
    CurlUrl='curl -X POST "https://api.fshare.vn/api/user/login" -H  "accept: application/json" -H  "User-Agent: %s" -H  "Content-Type: application/json" -d "{\\"user_email\\":\\"%s\\",\\"password\\":\\"%s\\",\\"app_key\\":\\"%s\\"}"' %(useragent, email, password, appkey)
    status, output = subprocess.getstatusoutput(CurlUrl)
    if "vip accounts only" in output:
        print("vip accounts only")
        return False, False
    token = json.loads(output.split('\n')[-1])['token']
    session_id = json.loads(output.split('\n')[-1])['session_id']
    return token, session_id

def main():
    url_folder = ''
    namefile = "fshare_links.txt"
    method = input("-help : show help\n")
    if method.split(' ')[0] == "-help":
        print("-link link_fshare : download link or folder\n-file path-to-file: download links from file")
        return
    elif method.split(' ')[0] == "-link":
        if "folder" in method.split(' ')[1].strip():
            url_folder = method.split(' ')[1].strip()
        else:
            url_link = method.split(' ')[1].strip()
    elif method.split(' ')[0] == "-file":
        namefile = method.split(' ')[1].strip()
    else:
        print("command not valid!")
        return
    with open('account.json', 'r') as acc:
        data = json.load(acc)
    password = data['password']
    email = data['user_email']
    useragent = data['useragent']
    appkey= data['app_key']
    #print(namefile)
    token, session_id = login(password, email, useragent, appkey)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if token is False:
        exit()
    if len(url_folder) < 2:
        if namefile != "fshare_links.txt":
            with open(namefile, "r") as fp:
                url_download = fp.readlines()
        else:
            url_download = [url_link]
    else:
        if layLinkFolder(url_folder, namefile, token, session_id, useragent) is False:
            exit()
        else:
            with open(namefile, "r") as fp:
                url_download = fp.readlines()
    for i in url_download:
        if "https" in i:
            link_ = i.split(' ')[0]
        else:
            link_ = "https://"+i.split(' ')[0]
        try:
            name_file = i.split(' ')[1].strip()
        except IndexError:
            name_file = link_.split('/')[4]
        if os.path.exists(dir_path+'/'+name_file) is True:
            print("file "+ name_file+" exist!")
            continue
        CurlUrl2 = 'curl -X POST "https://api.fshare.vn/api/session/download" -H  "accept: application/json" -H  "User-Agent: %s" -H  "Cookie: session_id=%s" -H  "Content-Type: application/json" -d "{\\"url\\":\\"%s\\",\\"password\\":\\"%s\\",\\"token\\":\\"%s\\",\\"zipflag\\":0}"' %(useragent, session_id, link_.strip(), password, token)
        status2, output2 = subprocess.getstatusoutput(CurlUrl2)
        print(output2, link_)
        download_link = json.loads(output2.split('\n')[-1])["location"]
        run_and_printchar(['wget','-nv',download_link])
        
if __name__ == '__main__':
    main()
