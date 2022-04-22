import pandas
aaa="PMSA-RCFC-1=1000,热段1补偿后的RCS流量,--------,--------,%²/kPa,7.2,150,0,3,6048,6080,61,69,32"
print(aaa.split(",",1))
print(aaa.split(",",13))
aa=",".join(aaa.split(",",13))
print(aa)
print(type(aa))

xl = pandas.ExcelFile("DDS清单模板-ZONG.xlsx")

sheet_names = xl.sheet_names
print(sheet_names)
print(type(sheet_names))
aaaaaaaaaaaaaaaa
bbbbbbbbbbbbbbbbbb
CCCCCCCCCCCCCCCCCCCCCCCCC