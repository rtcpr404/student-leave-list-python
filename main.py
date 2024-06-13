import pandas as pd
import datetime as date
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
# read files
df = pd.read_csv("data_leave.csv")
df2 = pd.read_csv("students(comma).csv")
# รวมไฟล์ data_leave กับ students(comma)
df3 = df.join(df2.set_index('id'), on='ID')
# รวมไฟล์ students(comma) กับ data_leave
df4 = df2.join(df.set_index('ID'), on='id')
def Main():
  print(
 '!! MUICT Student Leave System !!\n'
 '1. print a list of students\n'
 '2. submit a leave request\n'
 '3. check leave with class date\n'
 '4. check leave with student ID\n'
 '5. check leave with student first name\n'
 '6. print leave summary\n'
 '0. exit\n'
 'Option: ', end='')
def student_list(): #(1)
  data= pd.read_csv("students(comma).csv")
  print(data)
def data(): #(2)
  # input ID
  ID = int(input('ID: '))  
  # input type leave และเปลี่ยนตัวย่อเป็นชื่อเต็ม
  leave = input('Leave (S=Sick/B=Business/T=Travel/O=Others): ')
  if leave == 'S':
    leave = 'Sick'
  elif leave == 'B':
    leave = 'Business'
  elif leave == 'T':
    leave = 'Travel'
  elif leave == 'O':
    leave = 'Others'
  class_date = input('Class date (DD-MM-YYYY): ')
  # check date
  date_format = '%d-%m-%Y'
  signal = 0
 
  while signal == 0 :
    try:
      # แบ่งข้อมูลเป็น วัน-เดือน-ปี
      date.datetime.strptime(class_date, date_format)
      signal = 1
    except ValueError: 
      print("Incorrect data format, should be DD-MM-YYYY")
      class_date = input('Class date (DD-MM-YYYY): ')
  # เก็บข้อมูล
  data = {
      'ID': [ID],
      'Leave': [leave],
      'class_date': [class_date],
    }
  # check ID
  column = df2['id']
  check = False

  for i in column:
    if ID == int(i):    
      check = True
  if check :
    # ทำให้ข้อมูลอยู่ในรูปของ data frame
    df = pd.DataFrame(data)
    # เพิ่มข้อมูลลงในไฟล์ data_leave.csv
    df.to_csv('data_leave.csv', mode='a', index=False, header=False)
    print("-> La Dai La Pai Jaaa")
  else : 
    print('รหัสนักศึกษาไม่ถูกต้อง')
def chkbydate(): #(3)
  #input date
  chkdate = str(input())
  # loop count student leave
  sum = 0
  for i in range(len(list(df3['class_date']))):
    if chkdate == str(df3['class_date'][i]):
      sum += 1
  if sum == 0:
    print(f'There are 0 students leave on {chkdate}')
  else:
    print(f'There are {sum} students leave on {chkdate}')
  # loop print student name
  for i in range(len(list(df3['class_date']))):
    if chkdate == str(df3['class_date'][i]):
      print(f"({df3['Leave'][i]}) {df3['ID'][i]} {df3['fname'][i]} {df3['lname'][i]}")
      
def chkbyID(): #(4)
  #input ID
  chkID = str(input('ID: '))
  # loop print
  for i in range(len(list(df3['ID']))):
    if chkID == str(df3['ID'][i]):
      print(f"{df3['ID'][i]} {df3['fname'][i]} {df3['lname'][i]}: ({df3['Leave'][i]}) Leave on {df3['class_date'][i]}")
  else:
    print()                            

def chkbyfname(): #(5)
  # df4 but fname is all lower for check
  df5 = df4.copy()
  df5['fname'] = df5['fname'].str.lower()
  
  # input
  chkname = input('Firstname: ').lower()
  
  # data contain input
  l = df5[df5['fname'].str.contains(chkname)]
  
  if l.empty : # no this name in data
    print('There is no student found')
  else: # have name in data
    no_nan = l.copy()
    no_nan = no_nan[no_nan['Leave'].notnull()]
    
    if no_nan['Leave'].isnull().empty : # no leave date
      print('There is no student leave record')
      
    else: # have leave date
      # ตกแต่งการ print
      # ทำให้ตัวอักษรแรกของชื่อเป็นตัวใหญ่
      no_nan['fname'] = no_nan['fname'].str.capitalize()
      # เพิ่ม : หลัง lname
      no_nan['lname'] = no_nan['lname']+':'
      # เพิ่มวงเล็บให้ leave
      no_nan['Leave'] = '('+ no_nan['Leave'] + ')'
      # เพิ่ม Leave on หน้า class_date
      no_nan['class_date'] = 'Leave on '+no_nan['class_date']
      # ทำให้ข้อมูลไม่มี header and index
      no_nan = no_nan.to_string(index=False,header=False)
      print(no_nan)

def All_Leave(): #(6)
  # เลือกข้อมูลช่องที่ไม่ใช่ช่องว่าง
  df6 = (df4[df4['class_date'].notnull()])
  # เรียง index ใหม่
  df6 = df6.reset_index(drop=True)
  
  all_type = ['Sick','Business','Travel','Others']
  for i in all_type:
    print(f'--> {i}')
    
    p = df6[df6['Leave'].str.contains(i)]
    # ถ้าไม่มีการลาจะ print None
    if p.empty:
      print('None')
    # ถ้ามีการลาจะ print รายชื่อนักศึกษาทั้งหมด
    else:
      # ตกแต่งการ print
      # เพิ่ม : หลัง lname
      p['lname'] = p['lname']+':'
      # เพิ่ม Leave on หน้า class_date
      p['class_date'] = 'Leave on '+p['class_date']
      # ทำให้ข้อมูลไม่มี header and index และ drop leave type
      p = p.drop('Leave',axis=1).to_string(index=False,header=False)
      print(p)
    print()
M = 0
#----------------------------------------------------
# Main page

Main()
option = input()
while option != '0':
  if option == '1':
    student_list()
  elif option == '2':
    data()
  elif option == '3':
    chkbydate()
  elif option == '4':
    chkbyID()
  elif option == '5':
    chkbyfname()
  elif option == '6':
    All_Leave()
  else:
    print('Wrong option select!!\nPlease choose option again')
    option = input('Option: ')
  print('\n===========================================\n')
  Main()
  option = input()