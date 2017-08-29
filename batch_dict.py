#! /usr/bin/python3
'''
Created on Aug 28, 2017

@author: panb
'''

'''
Created on Aug 28, 2017

@author: panb
'''

import sys
import http.client
import json
import logging
import logging.handlers


# 设置日志
LOG_FILE = 'word_explain.log'  

  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024) # 实例化handler    
fmt = '%(asctime)s - %(message)s'  
  
formatter = logging.Formatter(fmt)   # 实例化formatter   
handler.setFormatter(formatter)      # 为handler添加formatter   
  
logger = logging.getLogger('getExplainFromYoudao')    # 日志文件名
logger.addHandler(handler)           # 为logger添加handler   
logger.setLevel(logging.DEBUG)

# 使用有道词典API查询一个单词的含义
def getExplain(word):
    # 有道词典API形如：
    # http://fanyi.youdao.com/openapi.do?keyfrom=batchtranslate&key=1679006548&type=data&doctype=json&version=1.1&q=process
    keyFrom='TEST1234556423'
    key='1161529587'
    youdao_api_url='/openapi.do?keyfrom='+keyFrom + '&key=' + key + '&type=data&doctype=json&version=1.1&q='
    conn = http.client.HTTPConnection("fanyi.youdao.com", 80)
    try:              
        conn.request("GET", youdao_api_url + word)
    except:
        conn = http.client.HTTPConnection("fanyi.youdao.com", 80)
        conn.request("GET", youdao_api_url + word)
    r1 = conn.getresponse()
    # 从返回的JSON字符串中提取出单词释义
    data1 = r1.read()
    jsonStr = data1.decode('utf-8')
    jsonObj = json.loads(jsonStr)
    if('basic' in jsonObj):
        explainObj = jsonObj['basic']['explains']
        firstExplainStr = '  '.join(explainObj)
        return firstExplainStr
    logger.warning('explain not found, word = ' + word)
    return 'NA' # 没有查到释义

def dealFile(fname):
    srcf = open(fname,"rt")
    dstf = open("result.txt", "wb")
    for word in srcf:
        word = word.rstrip('\n')
        explain = getExplain(word)
        dstf.write(bytes(word, 'utf_8'))
        dstf.write(bytes('|', 'utf-8'))
        dstf.write(explain.encode('utf_8'))
        dstf.write(bytes('\n', 'utf-8'))
        dstf.flush()
    dstf.close()

if __name__ == "__main__":
#     if len(sys.argv) != 2 :
#         print("usage: word2voice.py 单词文件")
#         sys.exit(1)
    dealFile("/home/panb/work/supermemo-tool/cet6_1.txt")
    
    