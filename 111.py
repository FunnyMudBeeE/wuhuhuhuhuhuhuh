import pandas as pd
def getDDSPointIndex(ddspoint:str,) -> int:
    pass
#需要对比的CU组态txt文件
txtpath = 'CU234.txt'
# txtpath = =input('请输入需要对比的CUtxt文件名')
#需要对比的PMS设置excel文件
xlpath = '附件1 DDS-PMS信号清单.xlsx'

#读取txt文件，保存为list对象，对象名lines
with open(txtpath,'r',encoding='utf-8',errors='ignore') as fread:
    lines = fread.readlines()

#定义输出对比结果的txt文件fwrite，用于保存对比结果
fwrite = open(r'resultD.txt','w')

#调用pandas读取excel内容，dafaframe对象类型，对象名exceldata，key = dds point
exceldata = pd.read_excel(xlpath,sheet_name="D",
                          dtype={'DDS POINT':str, 'PMS POINT1':str, 'PMS POINT2':str,
                                 'PMS POINT3':str,'PMS POINT4':str,'算法':str}).set_index('DDS POINT')
#逐行读取exceldata内容，查找是否在txt的行中



for indexs in exceldata.index:
    if not '_' in indexs:   #过滤PMS下划线点

        def cmplogic(suanfa,func1,func2):
            if exceldata.loc[indexs]['算法'] == suanfa:
                pmspoint1 = exceldata.loc[indexs]['PMS POINT1']
                pmspoint2 = exceldata.loc[indexs]['PMS POINT2']

                flag1 = False
                for line in lines:
                    cmpindex = str(indexs) + ','  # 加‘，’过滤点目录中的点名，点目录格式为点名=...
                    if cmpindex in line:
                        flag1 = True
                        tmpindex = lines.index(line)
                        inline = lines[tmpindex - 1]  # 找到IN的那一行，找块号用的

                        if 'In= ,B' in inline:  # 找到该点的引用块
                            startindex = inline.index('B')
                            endindex = inline.index('-')
                            findstr = inline[startindex + 1:endindex]
                            # findTag1 = False
                            # findTag2 = False

                            flag2 = False
                            for i in range(tmpindex + 30, tmpindex - 30, -1):  # 经验范围
                                newstr = func1 + findstr + ':'
                                if newstr in lines[i]:
                                    flag2 = True
                                    # print(newstr)
                                    if 'In= ,B' in lines[i + 1]:
                                        newline = lines[i + 1].split('B')
                                        for j in range(1, 3):
                                            try:
                                                newline[j] = newline[j].split('-', 1)[0]
                                            except:
                                                print('%s宏定义错误\n' % indexs)
                                                fwrite.write('%s宏定义错误\n' % indexs)
                                        flag3 = False
                                        flag4 = False
                                        for k in range(i + 50, i - 50, -1):
                                            if (func2 + newline[1] + ':') in lines[k]:
                                                # print(lines[k + 2])
                                                if pmspoint1 in lines[k + 2]:
                                                    print('%s——pmspoint1-%s对比正确\n' % (indexs, pmspoint1))
                                                    fwrite.write('%s——pmspoint1-%s对比正确\n' % (indexs, pmspoint1))
                                                    flag3 = True

                                        for k in range(i + 50, i - 50, -1):
                                            if (func2 + newline[2] + ':') in lines[k]:
                                                if (func2 + newline[2] + ':') in lines[k]:
                                                    # print(lines[k + 2])
                                                    if pmspoint2 in lines[k + 2]:
                                                        print('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                        fwrite.write('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                        flag4 = True
                                        if not flag3:
                                            print('%s——pmspoint1-%s对比错误\n' % (indexs, pmspoint1))
                                            fwrite.write('%s——pmspoint1-%s对比错误\n' % (indexs, pmspoint1))
                                        if not flag4:
                                            print('%s——pmspoint2-%s对比错误\n' % (indexs, pmspoint2))
                                            fwrite.write('%s——pmspoint2-%s对比错误\n' % (indexs, pmspoint2))
                                    else:
                                        print('%s点未连接-错误 \n' % (indexs))
                                        fwrite.write('%s点未连接-错误 \n' % (indexs))

                            if not flag2:
                                print('%s点对应的宏定义错误 \n' % (indexs))
                                fwrite.write('%s点对应的宏定义错误 \n' % (indexs))
                if not flag1:
                    print('%s找不到该点-错误 \n' % (indexs))
                    fwrite.write('%s找不到该点-错误 \n' % (indexs))


        if exceldata.loc[indexs]['算法'] == '0':  # 算法0 check
            pmspoint1 = exceldata.loc[indexs]['PMS POINT1']
            for line in lines:
                cmpindex = str(indexs) + ','  # 加‘，’过滤点目录中的点名，点目录格式为点名=...
                if cmpindex in line:
                    tmpindex = lines.index(line)
                    inline = lines[tmpindex - 1]  # 找到IN的那一行，找块号用的
                    if 'In= ,B' in inline:  # 找到该点的引用块
                        startindex = inline.index('B')
                        endindex = inline.index('-')
                        findstr = inline[startindex + 1:endindex]
                        findTag = False
                        if exceldata.loc[indexs]['信号类型'] == 'A':  # 模拟量情况下的检查
                            for i in range(tmpindex + 30, 30, -1):  # 经验范围
                                newstr = 'Func, PgAI, ' + findstr
                                # print(newstr)
                                if newstr in lines[i]:
                                    if pmspoint1 in lines[i + 2]:
                                        print('%s对比正确\n' % (indexs))
                                        fwrite.write('%s对比正确\n' % (indexs))
                                        findTag = True
                        elif exceldata.loc[indexs]['信号类型'] == 'D':  # 数字量情况下的检查
                            for i in range(tmpindex - 1, 30, -1):
                                newstr = 'Func, PgDI, ' + findstr
                                # print(newstr)
                                if newstr in lines[i]:
                                    if pmspoint1 in lines[i + 2]:
                                        print('%s对比正确\n' % (indexs))
                                        fwrite.write('%s对比正确\n' % (indexs))
                                        findTag = True
                        else:
                            print('%s信号类型错误\n' % (indexs))
                            fwrite.write('%s信号类型错误\n' % (indexs))
            if not findTag:
                print('%s对比错误——%s关系错误\n' % (indexs, pmspoint1))
                fwrite.write('%s对比错误——%s关系错误\n' % (indexs, pmspoint1))
        if exceldata.loc[indexs]['算法'] == '1': #算法1，4输入使用宏块D2TO1，2输入使用宏块D4TO1
            pmsindexlist =[]
            pmspoint1 = exceldata.loc[indexs]['PMS POINT1']
            pmspoint2 = exceldata.loc[indexs]['PMS POINT2']
            pmspoint3 = exceldata.loc[indexs]['PMS POINT3']
            pmspoint4 = exceldata.loc[indexs]['PMS POINT4']
            try:
                getlen = len(pmspoint3)
                getlen = len(pmspoint4)
                d4to1 = True #d2to1 = False ; D4to1 = True
            except TypeError:
                d4to1 = False
            if d4to1:

                for line in lines:
                    cmpindex = str(indexs) + ','   #加‘，’过滤点目录中的点名，点目录格式为点名=...
                    if cmpindex in line:
                        tmpindex = lines.index(line)
                        inline = lines[tmpindex-1] #找到IN的那一行，找块号用的
                        if 'In= ,B' in inline: #找到该点的引用块
                            startindex = inline.index('B')
                            endindex =  inline.index('-')
                            findstr = inline[startindex+1:endindex]
                            findTag1 = False
                            findTag2 = False
                            findTag3 = False
                            findTag4 = False
                            for i in range(tmpindex+30,tmpindex-30,-1):
                                newstr = 'Func, D4TO1, ' + findstr
                                if newstr in lines[i]:
                                    if 'In= ,B' in lines[i+1]:
                                        newline = lines[i+1].split('B')
                                        for j in range(1,5):
                                            try:
                                                newline[j]= newline[j].split('-',1)[0]
                                            except:
                                                print('%s宏定义错误\n' % indexs)
                                                fwrite.write('%s宏定义错误\n' % indexs)
                                    else:
                                        print('%s宏连接未找到对应定义\n' % indexs)
                                        fwrite.write('%s宏连接未找到对应定义\n' % indexs)
                                    for k in range(i+50,i-50,-1):
                                        if ('Func, PgDI, '+newline[1]) in lines[k]:
                                            if pmspoint1 in lines[k+2]:
                                                print('%s——pmspoint1-%s对比正确\n' %(indexs,pmspoint1))
                                                fwrite.write('%s——pmspoint1-%s对比正确\n' %(indexs,pmspoint1))
                                                findTag1 =True
                                        if ('Func, PgDI, ' + newline[2]) in lines[k]:
                                            if ('Func, PgDI, ' + newline[2]) in lines[k]:
                                                if pmspoint2 in lines[k + 2]:
                                                    print('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                    fwrite.write('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                    findTag2 = True
                                        if ('Func, PgDI, ' + newline[3]) in lines[k]:
                                            if ('Func, PgDI, ' + newline[3]) in lines[k]:
                                                if pmspoint3 in lines[k + 2]:
                                                    print('%s——pmspoint3-%s对比正确\n' % (indexs, pmspoint3))
                                                    fwrite.write('%s——pmspoint3-%s对比正确\n' % (indexs, pmspoint3))
                                                    findTag3 = True
                                        if ('Func, PgDI, ' + newline[4]) in lines[k]:
                                            if ('Func, PgDI, ' + newline[4]) in lines[k]:
                                                if pmspoint4 in lines[k + 2]:
                                                    print('%s——pmspoint4-%s对比正确\n' % (indexs, pmspoint4))
                                                    fwrite.write('%s——pmspoint4-%s对比正确\n' % (indexs, pmspoint4))
                                                    findTag4 = True
                                    if not findTag1:
                                        print('%s——pmspoint1-%s对比错误\n' %(indexs,pmspoint1))
                                        fwrite.write('%s——pmspoint1-%s对比错误\n' %(indexs,pmspoint1))
                                    if not findTag2:
                                        print('%s——pmspoint2-%s对比错误\n' % (indexs, pmspoint2))
                                        fwrite.write('%s——pmspoint2-%s对比错误\n' %(indexs,pmspoint2))
                                    if not findTag3:
                                        print('%s——pmspoint3-%s对比错误\n' % (indexs, pmspoint3))
                                        fwrite.write('%s——pmspoint3-%s对比错误\n' %(indexs,pmspoint3))
                                    if not findTag4:
                                        print('%s——pmspoint4-%s对比错误\n' % (indexs, pmspoint4))
                                        fwrite.write('%s——pmspoint4-%s对比错误\n' %(indexs,pmspoint4))
            else:
                for line in lines:
                    cmpindex = str(indexs) + ','  # 加‘，’过滤点目录中的点名，点目录格式为点名=...
                    if cmpindex in line:
                        tmpindex = lines.index(line)
                        inline = lines[tmpindex - 1]  # 找到IN的那一行，找块号用的
                        if 'In= ,B' in inline:  # 找到该点的引用块
                            startindex = inline.index('B')
                            endindex = inline.index('-')
                            findstr = inline[startindex + 1:endindex]
                            findTag1 = False
                            findTag2 = False
                            for i in range(tmpindex + 30, tmpindex - 30, -1):
                                newstr = 'Func, D2TO1, ' + findstr
                                if newstr in lines[i]:
                                    if 'In= ,B' in lines[i + 1]:
                                        newline = lines[i + 1].split('B')
                                        for j in range(1, 3):
                                            try:
                                                newline[j] = newline[j].split('-', 1)[0]
                                            except:
                                                print('%s宏定义错误\n' % indexs)
                                                fwrite.write('%s宏定义错误\n' % indexs)
                                    else:
                                        print('%s宏连接未找到对应定义-错误\n' % indexs)
                                        fwrite.write('%s宏连接未找到对应定义-错误\n' % indexs)
                                    for k in range(i + 50, i - 50, -1):
                                        if ('Func, PgDI, ' + newline[1]) in lines[k]:
                                            if pmspoint1 in lines[k + 2]:
                                                print('%s——pmspoint1-%s对比正确\n' % (indexs, pmspoint1))
                                                fwrite.write('%s——pmspoint1-%s对比正确\n' % (indexs, pmspoint1))
                                                findTag1 = True
                                        if ('Func, PgDI, ' + newline[2]) in lines[k]:
                                            if ('Func, PgDI, ' + newline[2]) in lines[k]:
                                                if pmspoint2 in lines[k + 2]:
                                                    print('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                    fwrite.write('%s——pmspoint2-%s对比正确\n' % (indexs, pmspoint2))
                                                    findTag2 = True
                                    if not findTag1:
                                        print('%s——pmspoint1-%s对比错误\n' % (indexs, pmspoint1))
                                        fwrite.write('%s——pmspoint1-%s对比错误\n' % (indexs, pmspoint1))
                                    if not findTag2:
                                        print('%s——pmspoint2-%s对比错误\n' % (indexs, pmspoint2))
                                        fwrite.write('%s——pmspoint2-%s对比错误\n' % (indexs, pmspoint2))

        if exceldata.loc[indexs]['算法'] == '2':
            cmplogic('2', 'Func, D2TO2, ', 'Func, PgDI, ')
        if exceldata.loc[indexs]['算法'] == '3':
            cmplogic('3','Func, TwoSel, ','Func, PgAI, ')
        if exceldata.loc[indexs]['算法'] == '4':
            cmplogic('4','Func, ATOH, ','Func, PgAI, ')
        if exceldata.loc[indexs]['算法']  == '5':
            cmplogic('5','Func, ATOL, ','Func, PgAI, ')