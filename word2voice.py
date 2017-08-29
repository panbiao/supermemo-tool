'''
Created on Aug 29, 2017

@author: panb
'''
#! /usr/bin/python
# coding=utf-8
#cUOFEkjKce5mYnP5fxEG5ISJLfE11/3hHe/voY7t70k=
import urllib2,xml.sax,sys
class ResponeHandler(xml.sax.ContentHandler):
    pron=0
    pronurl=None
    def startDocument(self):
        pass
    def startElement(self,tag,attributes):
        if tag != 'pron':return
        self.pron=1
    def endElement(self,tag):
        if tag != 'pron':return
        self.pron=0
    def characters(self,data):
        if(self.pron==1):
            print data
            self.pronurl = data

def Translator(word):
    #x = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #x.add_password(None,'http:','zxin10','zxin10')
    #auth = urllib2.ProxyBasicAuthHandler(x)
    #opener = urllib2.build_opener(auth)
    proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy2.zte.com.cn:80/'})
    opener = urllib2.build_opener( proxy_handler )

    #urllib2.install_opener(opener)
    searchword = word.replace(' ','+',10)
    print 'Search word:',searchword
    try:
        f=opener.open('http://dict-co.iciba.com/api/dictionary.php?w=%s' % searchword)
    except Exception:
        print 'Search word failed:',searchword
        ferror = open('e:\\script\\trans\\error.txt','a')
        ferror.write(searchword)
        ferror.write('\n')
        ferror.close()
        return
#    print f.read()
    print 'Search word success:',searchword    
    p=xml.sax.make_parser()
    handler = ResponeHandler()
    p.setContentHandler(handler)
    p.parse(f)
    if handler.pronurl:
        try:
            f=urllib2.urlopen(handler.pronurl)
            dstf = open('e:\\script\\trans\\%s.mp3' % word,"wb")
            BUFSIZE=8192
            while True:
                data = f.read(BUFSIZE)
                if not data : break
                dstf.write(data)
            dstf.close()
        except Exception:
            print 'Search word failed:',searchword
            ferror = open('e:\\script\\trans\\error.txt','a')
            ferror.write(searchword)
            ferror.write('\n')
            ferror.close()
            return        
#    print f.read()  
    
#    BUFSIZE=8192
#    while True:
#        data = f.read(BUFSIZE)
#        if not data : break
#        p.feed(data)
#    p.close()
    return

def DealFile(fname):
    srcf = open(fname,"rt")
    for word in srcf:
        word = word.rstrip('\n')
        Translator(word)

if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print "usage: word2voice.py 单词文件"
        sys.exit(1)
    DealFile(sys.argv[1])
    