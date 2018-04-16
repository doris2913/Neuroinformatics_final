# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 18:44:47 2017

@author: Doris
"""
import re
import urllib, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from http.cookiejar import CookieJar
from multiprocessing import Process, Queue
import multiprocessing as mp
import xlwt

global sheet1, wb

class Survey():
    def __init__(self):
        self.id = 'None'
        self.text = 'None'
        self.pType = 'None' # Present type: { 0:None; 1:Drink, 2:Cake, 3:Other }
        self.pNum = 0 # 抽幾個
        self.form = 'None' # 表單連結
        self.doneNum = 0 # 留言數目
        self.image = 0 # 有沒有圖片: { 0: 沒圖片, 1: 有圖片 }
        self.tag = 0 # 有沒有要tag人
        self.date = 'None' # 日期
        self.align = xlwt.easyxf('alignment: horizontal centre, vertical centre;')
    
    def __str__(self):
        return ("id={}\ntext={}\npType={}\ndoneNum={}".format(self.id, self.text, self.pType, self.doneNum))

    def parseText(self):
        tag = ['tag', 'Tag', 'TAG', u'標記', u'標註']
        if(any(word in self.text for word in tag)): #or u'標記' or u'標註'
            self.tag = 1
        if(u'抽' in self.text):
            self.pType = 'None'



    def writeXls(self, row, f):
        sheet1.write(row, 1, self.id, self.align)
        sheet1.write(row, 2, self.pType, self.align)
        sheet1.write(row, 3, self.doneNum, self.align)
        sheet1.write(row, 4, self.image, self.align)
        sheet1.write(row, 5, self.tag, self.align)
        sheet1.write(row, 6, self.date, self.align)
        #sheet1.write(row, 6, self.text, self.align)
        f.write(self.text)
        f.write('\n=======================================================\n')         

class Facebook():
    def __init__(self):
        self.email = # email
        self.password = # password
        self.fb_url = 'https://facebook.com/'
        self.login_url = 'https://m.facebook.com/'
        self.group_url = # group's url
        self.browser = webdriver.Firefox()
        self.maxSurvey = 200
        self.survey = []
        self.surNum = 0
        self.f = open("test.txt", "w", encoding='utf8')

    def login(self):
        self.browser.get(self.group_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(self.email)
        input_pass = self.browser.find_element_by_name('pass')
        input_pass.send_keys(self.password)
        input_pass.submit()
    
    def test(self):  # 留言
        #f = open('test.txt', 'w', encoding = 'utf8')
        self.login()
        # temp = self.browser.find_elements_by_xpath('//bodiv/div/span')
        time.sleep(4)
        while(self.surNum < 500):
            time.sleep(3)
            article = self.browser.find_elements_by_xpath('//body/div/div/div/div/div/div/div/div') # 每個PO文的頭(?
            artNum = len(article)
            for i in range(artNum-1):     # -1: 最後一個不要
                fbId = re.findall('mf_story_key\"\:\"(\d+)', article[i].get_attribute('data-ft'))[0]   # 每個PO文的ID (FB定的)
                context = article[i].find_element_by_xpath('./div/div/span')  # PO文內容
                # try: # 貼文有'更多'
                #     more = context.find_element_by_link_text(u'更多')
                # except NoSuchElementException:
                #     print('no')

                context = context.text
                if(u'問卷' in context):
                    self.survey.append(Survey())
                    self.survey[self.surNum].text = context
                    self.survey[self.surNum].id = fbId
                    date = article[i].find_element_by_xpath('.//div/div/abbr')  # PO文時間
                    self.survey[self.surNum].date = date.text
                    response = date.find_element_by_xpath('../following-sibling::div/a') # 留言
                    self.survey[self.surNum].doneNum = ("".join(re.findall('\d+', response.text))) # 留言數目

                    try: # 圖片
                        img = article[i].find_element_by_xpath('./div//a/img')
                        self.survey[self.surNum].image = 1
                        print("yes!", img.get_attribute('src'))
                    except NoSuchElementException:
                        print('no!')
                    (self.survey[self.surNum]).parseText() # 分析內文
                    (self.survey[self.surNum]).writeXls(self.surNum+1, self.f) # 寫檔
                    self.surNum += 1

            print(self.surNum)
            click = self.browser.find_element_by_link_text(u'查看更多貼文')
            click.click()
        #self.browser.quit()



def myPrint(fb):
    #a = (list(map(str, sur[:num])))
    print('b')
    f = open('test.txt', 'w', encoding = 'utf8')
    f.write('hello\n')
    processed = 0
    #while(q.get() != 'q'):
        #f.write('helloo\n')
        #f.write(str(q.get()))
    print(fb.surNum)
    #f.write(num)
    #f.write(a)
    f.close()

if(__name__ == '__main__'):
    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
   # wb.save('test.xls')
    #sheet1.write(0, 0, '0')
    all_centre_align = xlwt.easyxf('alignment: horizontal centre, vertical centre;')
    title = ['id', 'pType', 'doneNum', 'image', 'tag', 'date', 'completeText']
    for i in range(len(title)):
        sheet1.write(0, i+1, title[i], all_centre_align)
        sheet1.col(i+1).width = 256*20
    sheet1.col(7).width = 256*200    
    #q = Queue(maxsize = 0)
    fb = Facebook()
    #p = Process(target=myPrint, args = (fb, ))
    fb.test()
    wb.save('test.xls')
    #q.put('q')
    #p.start()
    #p.join()        
#myPrint(fb.survey)
#fb.printSurvey()