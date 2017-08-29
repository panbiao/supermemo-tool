#coding=utf-8

import os
import shutil
import sys

def writeCourseHead(fcourse):
	fcourse.write("<?xml version='1.0' encoding='utf-8'?>"+"\n")
	fcourse.write('''<course xmlns="http://www.supermemo.net/2006/smux">'''+"\n")
	fcourse.write("<guid>0782b5ac-5d2f-5fae-fc03d24a657b</guid>"+"\n")
	fcourse.write("<title>大学英语四六级词汇</title>"+"\n")
	fcourse.write("<created>2012-06-13</created>"+"\n")
	fcourse.write("<modified>2012-06-13</modified>"+"\n")
	fcourse.write("<language-of-instruction>en</language-of-instruction>"+"\n")
	fcourse.write("<default-items-per-day>30</default-items-per-day>"+"\n")
	fcourse.write("<default-template-id>0</default-template-id>"+"\n")
	fcourse.write("<type>regular</type>"+"\n")
	fcourse.write("<default-items-per-day>30</default-items-per-day>"+"\n")
	fcourse.write("<author>潘纪洵</author>"+"\n")
	fcourse.write("<rights-owner>潘纪洵</rights-owner>"+"\n")
	fcourse.write('''<description lang="en">本课程为潘纪洵制作</description>'''+"\n")
	fcourse.write("<translators>潘纪洵</translators>"+"\n")
	fcourse.write("<box-link>www.emagic.org.cn</box-link>"+"\n")
	fcourse.write("<version>1.0.3531</version>"+"\n")
	fcourse.write('''<define-subtype enabled="true" id="1" name="回忆释义"/>'''+"\n")

def writeCourseTail(fcourse):
	fcourse.write('''</course>'''+"\n")

def writeItemHead(fitem, chapter):
	fitem.write('''<?xml version="1.0" encoding="utf-8"?>'''+"\n")
	fitem.write('''<item xmlns="http://www.supermemo.net/2006/smux">'''+"\n")
	fitem.write('''  <lesson-title>大学英语四六级词汇</lesson-title>'''+"\n")
	fitem.write('''  <chapter-title>''' + chapter +'''</chapter-title>'''+"\n")
	fitem.write('''  <question-title>根据单词,回忆释义</question-title>'''+"\n")

def writeItemTail(fitem):
	fitem.write('''  <question-audio>true</question-audio>'''+"\n")
	fitem.write('''  <modified>2012-06-13</modified>'''+"\n")
	fitem.write('''<template-id>15</template-id>'''+"\n")
	fitem.write('''<gfx-1 id="53" group-id="1" />'''+"\n")
	fitem.write('''</item>'''+"\n")

def dealListFile(list_file_name, output_path):
	print list_file_name
	flist = open(list_file_name, 'r')
	course = output_path + "/course.xml"
	fcourse = open(course, 'w')
	writeCourseHead(fcourse)

	for line in flist.readlines():
#		print line
		wid = line.split("|")[0]
		word = line.split("|")[1]
		phonetic = line.split("|")[2]
		translation = line.split("|")[3]
		chapter = line.split("|")[4]
# 		print "wid=", wid
# 		print "word=", word
# 		print "phonetic=", phonetic
# 		print "translation", translation
		course_line = '''  <element subtype="1" type="exercise" id="'''+wid+'''" name="'''+word+'''"/>'''
		fcourse.write(course_line+"\n")
		
		#create item file
		wid_str = "000000"+wid
		wid_str = wid_str[-5:]
		item = output_path + "/item"+wid_str+".xml"
		fitem = open(item, 'w')
		writeItemHead(fitem, chapter)
		question_line='''<question><big><b>'''+word+'''</b></big>　　　'''+phonetic+'''</question>'''
		fitem.write(question_line+"\n")
		answer_line='''<answer><kbd>''' + translation + '''</kbd></answer>'''
		fitem.write(answer_line+"\n")
		writeItemTail(fitem)
		fitem.close()
		
		#copy wav file
		src_wav = '''d:\\speech\\'''+word[0]+'''\\'''+word+'''.mp3'''
		dst_wav = output_path + "\\media\\" + wid_str +"q.mp3"
		if os.path.exists(src_wav):
			shutil.copy(src_wav, dst_wav)
		else:
			print src_wav + " isn't exist"
			
		
	writeCourseTail(fcourse)	
	fcourse.close()
	flist.close()

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print sys.argv[0]+" word_list_file output_path"
		sys.exit()
	if (os.path.exists(sys.argv[2])):
		shutil.rmtree(sys.argv[2])
	os.mkdir(sys.argv[2])
	os.mkdir(sys.argv[2]+"/media")
	dealListFile(sys.argv[1], sys.argv[2])