# encoding=utf-8
import jieba
import xlwt

jieba.set_dictionary('dict.txt.big')
jieba.load_userdict("userdict.txt")

f = open("test.txt", "r", encoding='utf8')
f_out = open("out.txt", "w", encoding='utf8')

sen = f.read()
sen1 = sen.split('=======================================================')
# f_out.write(sen1[0])
# f_out.write("\n")

food = [u'迷客夏', u'飲品', u'飲料', u'九品川', u'星巴克', u'十杯', u'蛋糕', u'甜品', u'甜點', u'Coco', u'Cocobrownies', u'cocobrownies', u'布朗尼']
money = [u'現金', u'禮卷']
ticket = [u'電影票', u'電影', u'電影票']

wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Sheet')
all_centre_align = xlwt.easyxf('alignment: horizontal centre, vertical centre;')


for m in range(len(sen1)):
	temp = []
	ptype = ''
	f_out.write(",".join(list((jieba.cut(sen1[m])))))

	# words = list(jieba.cut(sen1[m]))
# 	try:
# 		i = words.index(u'抽')
# 	except:
# 		ptype = 'None'
# 		continue


	
# 	for j in range(10):
# 		if(len(words) <= i+j):
# 			break
# 		if(words[i+j] in drink):
# 			ptype += 'drink '
# 		if(words[i+j] in dessert):
# 			ptype += 'dessert '
# 		if(words[i+j] in money):
# 			ptype += 'money'
# 		if(words[i+j] in ticket):
# 			ptype += 'ticket'

# 	if(ptype == ''):
# 		ptype = 'other'
# 	sheet1.write(m, 1, ptype)
# 		#f_out.write(words[i+j])
# 		#f_out.write("\n")
# wb.save('type.xls')

# f.close()
# f_out.close()