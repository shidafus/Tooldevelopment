import xlsxwriter

workbook = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\运维工程师-06月考核计划.xlsx1')  # 创建一个Excel文件
worksheet = workbook.add_worksheet('绩效考核表')  # 创建一个工作对象

# worksheet.set_column('A:A', 20)  # 设定第一列(A)宽度为20像素
bold = workbook.add_format({'bold': True})  # 定义一个加粗的格式对象

worksheet.write('D26', u'环境支撑', bold)  # A1单元格写入'Hello'
worksheet.write('E26', u'异常处理与业务熟悉(即时通讯,客服系统)', bold)  # A2单元格写入'World'并引用加粗格式
worksheet.write('G26', u'在收到需求的同时,解决需求,并加深对业务系统熟悉程度', bold)  # B2 写入中文并引用加粗格式

worksheet.write('D28', u'运维效率', bold)
worksheet.write('G26', u'熟悉,python自动化脚本,提升日常运维效率', bold)
worksheet.write('G29', u'开发python运维工具脚本', bold)

chart = workbook.add_chart({type, 'column'})
worksheet.insert_chart('A7', chart)
# worksheet.write(2, 0, 32)  # 用行列表示法写入数字 '32' 与 '35.5'
# worksheet.write(3, 0, 35.5)  # 行列表示法的单元格下标以0作为起始值, '3, 0' 等价于 A3
# worksheet.write(4, 0, '=SUM(A3:A4)')  # 求A3 和A4 的和, 并将结果写入 '4, 0'

# worksheet.insert_image('B5', 'img/python-logo.png')
workbook.close()