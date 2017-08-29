'''
Created on Aug 29, 2017

@author: panb
'''

# coding=utf-8

import sys
import time
import string

TOKEN_NULL = 0
TOKEN_ID = 1
TOKEN_QUE = 2
TOKEN_ANS = 3
TOKEN_TYPE = 4

TOKEN_GRAPH = 11
TOKEN_TABLE = 12
TOKEN_MULTI = 13
TOKEN_JUDGE = 14
TOKEN_ORDER = 15
TOKEN_CHOICE = 16
TOKEN_FILL = 17
TOKEN_MATCH = 18
TOKEN_RBRACE = 101
TOKEN_LSBRACK = 102
TOKEN_RSBRACK = 103
TOKEN_STRING = 104
TOKEN_LINEEND = 105
TOKEN_COMMENT = 106
PARSE_SUCC = 0
PARSE_FAIL = 1

class Parser:
    def __init__(self):
        self.current_pos = 0
        self.remainder = ""
        self.remainder_last = ""
        self.itemid=""
        self.question=""
        self.answer=""
        self.itemtype = 0
        
    def next_token(self):
        self.remainder_last = self.remainder
        if (len(self.remainder) == 0):
            return (TOKEN_NULL, None)
        if (self.remainder[0:1] == '''#'''):
            line_len = self.remainder.find('''\n''')
            if (line_len < 0):
                line_len = len(self.remainder)
            self.remainder = self.remainder[line_len:]
            return (TOKEN_COMMENT, None)
        if (self.remainder[0:2] == '''I:'''):           
            self.remainder = self.remainder[2:]
            return (TOKEN_ID, None)
        if (self.remainder[0:2] == '''Q:'''):
            self.remainder = self.remainder[2:]
            return (TOKEN_QUE, None)
        if (self.remainder[0:2] == '''A:'''):
            self.remainder = self.remainder[2:]
            return (TOKEN_ANS, None)
        if (self.remainder[0:2] == '''T:'''):
            self.remainder = self.remainder[2:]
            return (TOKEN_TYPE, None)        
        if (self.remainder[0:1] == '\r' or self.remainder[0:1] == '\n'):
            self.remainder = self.remainder[1:]
            if (self.remainder[0:1] == '\r' or self.remainder[0:1] == '\n'):
                self.remainder = self.remainder[1:]
            return (TOKEN_LINEEND, None)
        if (self.remainder[0:1] == '''{'''):
            if (self.remainder[1:3] == '''g:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_GRAPH, None)
            if (self.remainder[1:3] == '''t:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_TABLE, None)
            if (self.remainder[1:3] == '''m:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_MULTI, None)
            if (self.remainder[1:3] == '''j:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_JUDGE, None)
            if (self.remainder[1:3] == '''0:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_ORDER, None)
            if (self.remainder[1:3] == '''l:'''):
                self.remainder = self.remainder[3:]
                return (TOKEN_MATCH, None)
            if (self.remainder[1:2] == '''['''):
                self.remainder = self.remainder[1:]
                return (TOKEN_CHOICE, None)
            self.remainder = self.remainder[1:]
            return (TOKEN_FILL, None)
        if (self.remainder[0:1] == '''}'''):
            self.remainder = self.remainder[1:]
            return (TOKEN_RBRACE, None)
#         if (self.remainder[0:1] == '''['''):
#             self.remainder = self.remainder[1:]
#             return (TOKEN_LSBRACK, None)
#         if (self.remainder[0:1] == ''']'''):
#             self.remainder = self.remainder[1:]
#             return (TOKEN_RSBRACK, None)
        line_len = self.remainder.find('''\n''')
        if (line_len < 0):
            line_len = len(self.remainder)
        pos1 = self.remainder.find('''{''', 0, line_len)
        pos2 = self.remainder.find('''}''', 0, line_len)
        pos3 = self.remainder.find('''[''', 0, line_len)
        pos4 = self.remainder.find(''']''', 0, line_len)
        endpos = line_len
        if (pos1 >0 and endpos > pos1):
            endpos = pos1
        if (pos2 >0 and endpos > pos2):
            endpos = pos2
        if (pos3 >0 and endpos > pos3):
            endpos = pos3
        if (pos4 >0 and endpos > pos4):
            endpos = pos4
        token_len = endpos
        token_value = self.remainder[0:token_len]
        self.remainder = self.remainder[token_len:]
        return (TOKEN_STRING, token_value)

    def rollback_token(self):
        self.remainder = self.remainder_last
    
    def peep_input(self, num=1):
        if (len(self.remainder) > num):
            return self.remainder[0:num]
        else:
            return self.remainder
    
    def read_input(self, num=1): 
        if (len(self.remainder) > num):
            ret_value = self.remainder[0:num]
            self.remainder = self.remainder[num:]
            return ret_value
        else:
            ret_value = self.remainder
            self.remainder = ""
            return ret_value
        
    def parse_graph(self):
        result_str = '' 
        (token_type1, token_value1) = self.next_token()
        (token_type2, token_value2) = self.next_token()        
        if (token_type1 != TOKEN_STRING or token_type2 != TOKEN_RBRACE):
            return (PARSE_FAIL, None)
        if (token_value1.find(',') > 0):
            fields =  token_value1.split(",")
            result_str = '<gfx item-id="' + fields[0] + '"' + ' file="' + fields[1] + '"/>'
        else:
            result_str = '<gfx file="' + token_value1 + '"/>'
        return (PARSE_SUCC, result_str)
    
    def parse_table_row(self, rowstr):
        field_cnt = rowstr.count('''|''')
        result_str = ''
        if (field_cnt > 0):
            fields = rowstr.split('''|''')
            field_no = 0
            result_str = '''<tr>'''
            while (field_no <= field_cnt):
                field = fields[field_no]
                result_str = result_str + '''<td'''
                if (field.startswith('''+''')):
                    field = field[1:]
                    if (field[0:1].isdigit()):
                        result_str = result_str + ''' rowspan="''' + field[0:1] + '''"'''
                        field = field[2:]
                    else:
                        field = field[1:]
                    if (field[0:1].isdigit()):
                        result_str = result_str + ''' colspan="''' + field[0:1] + '''"'''
                        field = field[1:]
                result_str = result_str + '''>''' + field + '''</td>'''
                field_no = field_no + 1
            result_str = result_str + '''</tr>'''
        return result_str
    
    def parse_table(self):
        result_str = '''<table border="1" cellpadding="0" cellspacing="0"><tbody>\n'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            result_str = result_str + self.parse_table_row(parse_value)
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''\n'''                
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''</tbody></table>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)
    
    def parse_choice(self):
        result_str = '''<radio display="inline">'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            parse_value = parse_value.replace('''[=''', '''<option correct="true">''')
            parse_value = parse_value.replace('''[''', '''<option>''')
            parse_value = parse_value.replace(''']''', '''</option>''')
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''                
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''</radio>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)
    
    def parse_multi(self):
        result_str = '''<checkbox display="inline">'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            parse_value = parse_value.replace('''[=''', '''<option correct="true">''')
            parse_value = parse_value.replace('''[''', '''<option>''')
            parse_value = parse_value.replace(''']''', '''</option>''')
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''</checkbox>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)
    
    def parse_fill(self):
        result_str = '''<spellpad correct="'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''"/>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)
        
    def parse_order(self):
        result_str = '''<ordering-list orientation="horizontal">'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            parse_value = parse_value.replace('''[''', '''<option>''')
            parse_value = parse_value.replace(''']''', '''</option>''')
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''</ordering-list>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)        
    
    def parse_judge(self):
        result_str = '''<true-false true="正确" false="错误" correct="'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''" labels="true"/>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str) 

    def parse_match(self):
        result_str = '''<drag-drop orientation="horizontal" dropsign="10"><drop-text>'''
        parse_code = 0
        parse_value = ''
        while(True):
            (parse_code, parse_value) = self.parse_express()
            answer_cnt = parse_value.count('''[=''')
            while (answer_cnt > 0):
                (word1,word_tmp,word2) = parse_value.partition('''[=''')
                word2 = word2.replace(''']''', '''-}''', 1)
                parse_value = word1 + '''{-''' + word2
                answer_cnt = answer_cnt -1
            parse_value = parse_value.replace('''[''', '''</drop-text><option>''', 1)
            parse_value = parse_value.replace('''[''', '''<option>''')
            parse_value = parse_value.replace(''']''', '''</option>''')
            parse_value = parse_value.replace('''{-''', '''[''')
            parse_value = parse_value.replace('''-}''', ''']''') 
                
            result_str = result_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                result_str = result_str + '''<br/>\n'''
            elif (token_type == TOKEN_RBRACE):
                result_str = result_str + '''</drag-drop>'''
                break
            else:
                parse_code = PARSE_FAIL
                break        
        return (parse_code, result_str)
    
    def parse_express(self):
        express_str = ""
        parse_code=0
        parse_value=""
        while (True):
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_NULL):
                break
            elif (token_type == TOKEN_STRING):
                parse_value = token_value
            elif (token_type == TOKEN_GRAPH):
                (parse_code, parse_value) = self.parse_graph()
            elif(token_type == TOKEN_TABLE):
                (parse_code, parse_value) = self.parse_table()
            elif(token_type == TOKEN_CHOICE):
                (parse_code, parse_value) = self.parse_choice()
            elif(token_type == TOKEN_MULTI):
                (parse_code, parse_value) = self.parse_multi()
            elif(token_type == TOKEN_FILL):
                (parse_code, parse_value) = self.parse_fill()
            elif(token_type == TOKEN_ORDER):
                (parse_code, parse_value) = self.parse_order()
            elif(token_type == TOKEN_JUDGE):
                (parse_code, parse_value) = self.parse_judge()
            elif(token_type == TOKEN_MATCH):
                (parse_code, parse_value) = self.parse_match()
            else:
                self.rollback_token()
                break

            express_str = express_str + parse_value

        return (parse_code, express_str)
    
    def parse_id(self):
        (token_type, token_value) = self.next_token()
        parse_code = PARSE_FAIL
        str_id = ""
        if (token_type == TOKEN_STRING):
            str_id = token_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                parse_code = PARSE_SUCC
        return (parse_code, str_id)
    
    def parse_question(self):
        parse_code=0
        parse_value = ''
        question_str = ''
        while (True):
            parse_code, parse_value = self.parse_express()
            if (parse_code != PARSE_SUCC):
                break
            question_str = question_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                if (len(question_str) > 0):
                    question_str = question_str + '''<br/>\n'''
            elif (token_type == TOKEN_COMMENT):
                pass
            else:
                self.rollback_token()                
                break 
        return (parse_code, question_str)

    def parse_answer(self):
        parse_code=0
        parse_value = ''
        answer_str = ''
        while (True):
            parse_code, parse_value = self.parse_express()
            if (parse_code != PARSE_SUCC):
                break
            answer_str = answer_str + parse_value
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                if (len(answer_str) > 0):
                    answer_str = answer_str + '''<br/>\n'''
            elif (token_type == TOKEN_COMMENT):
                pass
            else:                
                break 
        return (parse_code, answer_str)

    def parse_type(self):
        (token_type, token_value) = self.next_token()
        parse_code = PARSE_FAIL
        itemtype = 0
        if (token_type == TOKEN_STRING):
            itemtype = int(token_value)
            (token_type, token_value) = self.next_token()
            if (token_type == TOKEN_LINEEND):
                parse_code = PARSE_SUCC
        return (parse_code, itemtype)
        
    def parse(self, content):
        self.remainder = content
        self.remainder_last = content
        self.current_pos = 0
        self.itemid=""
        self.question=""
        self.answer=""
        self.itemtype = 0
        parse_code=0
        while (True):
            (token_type, token_value) = self.next_token()
            print token_type, token_value
            if (token_type == TOKEN_NULL):
                break    
            if (token_type == TOKEN_ID):
                parse_code, self.itemid = self.parse_id()
            elif (token_type == TOKEN_QUE):
                parse_code, self.question = self.parse_question()
            elif (token_type == TOKEN_ANS):
                parse_code,  self.answer = self.parse_answer()
            elif (token_type == TOKEN_TYPE):
                parse_code, self.itemtype = self.parse_type()
            elif (token_type == TOKEN_COMMENT):
                pass
            else:
                parse_code = PARSE_FAIL
            
            if (parse_code != PARSE_SUCC):
                print "parse fail:", self.remainder, token_value
                break
        return parse_code

def string_preprocess(word):
    word=string.replace(word,'''&''', '''&amp;''')
    word=string.replace(word,'''>''', '''&gt;''')
    word=string.replace(word,'''<''', '''&lt;''')
    word=string.replace(word,"""'""", '''&apos;''')  #replace '
    word=string.replace(word,'''"''', '''&quot;''')   #replace "
    word=string.replace(word,'''{{''', '''<''')
    word=string.replace(word,'''}}''', '''>''')
    return word

def CreateXML(item, qtype, que, ans):
    name = '''item'''+ item
    fcourse = open("course.xml", "at")
    if (qtype == "100"):
        fcourse.write('''    <element id="''' + item +'''" type="pres" disabled="true" name="''' + name +'''" >''' + "\n")
    elif (qtype == "101"):
        fcourse.write('''    </element>''' + "\n")
        return
    else:
        fcourse.write('''        <element id="''' + item +'''" type="exercise" name="''' + name +'''" />''' + "\n")
    fcourse.close()
    
    item = item.zfill(5)
    filename = "item" + item + ".xml"        
    fxmlfile = open(filename, "wt")    
    fxmlfile.write('''<?xml version="1.0" encoding="utf-8"?>''' + "\n")
    fxmlfile.write('''<item xmlns="http://www.supermemo.net/2006/smux">''' + "\n")
    fxmlfile.write('''  <lesson-title></lesson-title>''' + "\n")
    fxmlfile.write('''  <chapter-title></chapter-title>''' + "\n")
    fxmlfile.write('''  <question-title></question-title>''' + "\n")
    fxmlfile.write('''  <question><big><b>''' + que +'''</b></big></question>''' + "\n")
    fxmlfile.write('''  <answer><kbd>''' + ans + '''</kbd></answer>''' + "\n")
    fxmlfile.write('''  <modified>2014-03-27</modified>''' + "\n")
    fxmlfile.write('''  <template-id>15</template-id>''' + "\n")
    fxmlfile.write('''  <question-audio>true</question-audio>''' + "\n")
    fxmlfile.write('''  <gfx-1 id="53" group-id="1" />''' + "\n")
    fxmlfile.write('''</item>''' + "\n")
    fxmlfile.close()

def OutputCourseHead(guid, titile):
    createtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    fcourse = open("course.xml", "wt")
    fcourse.write('''<?xml version='1.0' encoding='utf-8'?>''' + "\n")
    fcourse.write('''<course xmlns="http://www.supermemo.net/2006/smux">''' + "\n")
    fcourse.write('''  <guid>''' + guid + '''</guid>''' + "\n")
    fcourse.write('''  <title>''' + titile + '''</title>''' + "\n")
    fcourse.write('''  <created>''' + createtime + '''</created>''' + "\n")
    fcourse.write('''  <modified>''' + createtime + '''</modified>''' + "\n")
    fcourse.write('''  <language-of-instruction>en</language-of-instruction>''' + "\n")
    fcourse.write('''  <default-items-per-day>30</default-items-per-day>''' + "\n")
    fcourse.write('''  <default-template-id>0</default-template-id>''' + "\n")    
    fcourse.write('''  <type>regular</type>''' + "\n")
    fcourse.write('''  <default-items-per-day>30</default-items-per-day>''' + "\n")
    fcourse.write('''  <author>panbiao</author>''' + "\n")
    fcourse.write('''  <version>1.0.3531</version>''' + "\n")
    fcourse.write('''  <define-subtype id="2" name="subtype"/>''' + "\n")
    fcourse.write('''  <define-subtype enabled="true" id="1" name="subtype"/>''' + "\n")
    fcourse.write('''  <element subtype="1" type="pres" id="1" disabled="true" name="subtype">''' + "\n")
    fcourse.close()
    
def DealFile(fname):
    fsrc = open(fname,"rt")
    line = fsrc.readline()
    title = line[6 :]
    title = title.rstrip('\n')
    line = fsrc.readline()
    guid = line[5 :]
    guid = guid.rstrip('\n')
    line = fsrc.readline()
    ischemistry = line[10 :]
    ischemistry = ischemistry.rstrip('\n')
    line = fsrc.readline()

    OutputCourseHead(guid, title)
    
    lex = Parser()
    lines = fsrc.readlines()
    rawstr = ''
    for word in lines:
        word = word.strip(" ")
        if (word == "\n"):  #encounter a sepator, a item end,try create item
            if (rawstr == ""): #the item has no content
                continue
            rawstr = string_preprocess(rawstr)            
            ret_code = lex.parse(rawstr)
            if (ret_code == PARSE_SUCC):
                CreateXML(lex.itemid, lex.itemtype, lex.question, lex.answer)
            rawstr = ''
        else:            
            rawstr = rawstr + word
    fcourse = open("course.xml", "at")
    fcourse.write('''  </element>''' + "\n")
    fcourse.write('''</course>''' + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print "usage: txt2sm.py qafile"
        sys.exit(1)
    DealFile(sys.argv[1])    
