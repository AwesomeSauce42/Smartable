import numpy as np
from flask import Flask, request, render_template , redirect,url_for
import pickle
import pandas as pd
import re
import hashlib
import ipywidgets as widgets
from IPython.display import display
from io import StringIO
from datetime import datetime, timedelta


course_picked=[]
app = Flask(__name__,template_folder='C:/Users/shash/Downloads/admin/smartable/', static_url_path='/static', static_folder='static')
# app = Flask(__name__, template_folder='C:/Users/shash/Downloads/admin/smartable/')

# timetable = pd.read_excel('C:/Users/shash/Downloads/admin/smartable/timetable.xlsx')
timetable = pd.read_excel('timetable.xlsx')
table = timetable.to_html()


@app.route('/excel-table')
def excel_table():
    return table

user_data = pd.read_excel('C:/Users/shash/Downloads/admin/smartable/users.xlsx', index_col='Email')

def process_login(email, password):
    """
    Check if the email and password are valid
    """
    if email not in user_data.index:
        return False
    else:
        stored_password = user_data.loc[email, 'Password']
        if hashlib.sha256(password.encode()).hexdigest() == stored_password:
            return True
        else:
            print("Password incorrect")
            return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])


def login():
    correct = ""
    return render_template('login.html',correct = correct)

@app.route('/log_in', methods=['POST'])
def log_in():
    email = request.form['email']
    password = request.form['password']

    if process_login(email, password):
        print(user_data.loc[email])
        user=user_data.loc[email]
        access = user[5]
        if access == 0:
            return render_template('accounts.html', first_name = user[0], last_name = user[1], email = email, phone_number = user[3]
                                , roll_number = user[4],courses_registered_in = user[5])
        else:
            return render_template('admin.html', first_name = user[0], last_name = user[1], email = email, phone_number = user[3]
                               , roll_number = user[4],courses_registered_in = user[5])
    else:
        correct = "Incorrect Email ID and Password"
        print(email, " ", password)
        return render_template('login.html',correct = correct)

    
ALL = 'ALL'
def unique_sorted_values_plus_ALL(array):
    unique = array.unique().tolist()
    # unique.insert(0, ALL)
    return unique

def dropdown_major_eventhandler(change):
    print("hello")
    if (change == ALL):
        print(timetable)
    else:
        Major_courses = timetable.loc[timetable.Major == change]
        print(change)
        course = Major_courses.iloc[:, [0,1]]
        print(course.drop_duplicates())
        return (course.drop_duplicates())

def capture(func):
    out = StringIO()
    output = out.getvalue()
    out.close()
    return output

@app.route('/predict')
def predict():
    output=unique_sorted_values_plus_ALL(timetable.Major)
    print(output)
    return render_template('products.html', out=output,my_dict={},subjects=[],uwe = list_cour)


dic_day = {"M": 0, "T": 1, "W": 2, "F": 4, "S": 5}

def add_to_table(data, day, Dict): 
    st = data[3]
    end = data[4]
    time_st = '16/4/2020 '+str(st)
    date_format = '%d/%m/%Y %H:%M:%S'
    given_time_st = datetime.strptime(time_st, date_format)
    time_end = '16/4/2020 '+str(end)
    given_time_end = datetime.strptime(time_end, date_format)
    while given_time_st < given_time_end:
        string = str(given_time_st)
        Dict[string[11:]].pop(dic_day[day])
        Dict[string[11:]].insert(dic_day[day], data[1])
        if day == "T":
            Dict[string[11:]].pop(dic_day[day] + 2)
            Dict[string[11:]].insert(dic_day[day] + 2, data[1])
        given_time_st += timedelta(minutes=30)
    return Dict


list_cour = ['ALL','CHD','ENG','SOC','ENF','ECO','BMS','CSD','ECE','EEE','PHY','BIO','HIS','INT','CED','MAT','CHY']
# ccc_list = ['CCC222','CCC228','CCC337','CCC345','CCC402','CCC407','CCC409','CCC416','CCC417','CCC419','CCC423','CCC441','CCC442','CCC515','CCC606','CCC614','CCC634','CCC639','CCC670','CCC675','CCC676','CCC677','CCC678','CCC679','CCC724','CCC801','CCC80']

tt = {}
# cou
lt2=[]
subjects2 = []

course = ''
fin_list2=[]
global sub1
global cour1
@app.route('/predict2/<c_name>')
def predict2(c_name):
    global course
    global lt
    global tt
    global subjects2
    global fin_list
    
    ccc_courses = timetable.loc[(timetable['Course Code'].str.contains("CCC", na=False))& (timetable['Component'] == "LEC1") ]
    ccc_courses = ccc_courses.iloc[:, [0,1,5,6,7]]

    
    
    
    

    print(type(c_name),"Namaste")
    course = c_name
    print(course,"Namaste")
    course_details=[]
    course_picked = []
    course_picked.append(c_name)
    print((c_name))
    subject = c_name
    major_course = timetable.loc[(timetable['Type'] == 'Major') & (timetable['Major'].str.contains(subject))  & (timetable['Component'] == "LEC1")]
    subject = major_course.iloc[:, [0,1,5,6,7]]
    final = subject.drop_duplicates()
    lt = final.values.tolist()
    lt2=lt

    Dict = {"08:00:00": [' ---- ' for j in range(7)] , "08:30:00": [' ---- ' for j in range(7)],
       "09:00:00": [' ---- ' for j in range(7)] , "09:30:00": [' ---- ' for j in range(7)],
       "10:00:00": [' ---- ' for j in range(7)] , "10:30:00": [' ---- ' for j in range(7)],
       "11:00:00": [' ---- ' for j in range(7)] , "11:30:00": [' ---- ' for j in range(7)],
       "12:00:00": [' ---- ' for j in range(7)] , "12:30:00": [' ---- ' for j in range(7)],
       "13:00:00": [' ---- ' for j in range(7)] , "13:30:00": [' ---- ' for j in range(7)],
       "14:00:00": [' ---- ' for j in range(7)] , "14:30:00": [' ---- ' for j in range(7)],
       "15:00:00": [' ---- ' for j in range(7)] , "15:30:00": [' ---- ' for j in range(7)],
       "16:00:00": [' ---- ' for j in range(7)] , "16:30:00": [' ---- ' for j in range(7)],
       "17:00:00": [' ---- ' for j in range(7)] , "17:30:00": [' ---- ' for j in range(7)],
       "18:00:00": [' ---- ' for j in range(7)] , "18:30:00": [' ---- ' for j in range(7)],
       "19:00:00": [' ---- ' for j in range(7)] , "19:30:00": [' ---- ' for j in range(7)],
       "20:00:00": [' ---- ' for j in range(7)]}
    
    for each in lt:
        if "M" in each[2]:
            Dict = add_to_table(each, "M", Dict)
        if "T" in each[2]:
            Dict = add_to_table(each, "T", Dict)
        if "W" in each[2]:
            Dict = add_to_table(each, "W", Dict)
        if "F" in each[2]:
            Dict = add_to_table(each, "F", Dict)
        if "S" in each[2]:
            Dict = add_to_table(each, "S", Dict)
    c_list = []
    for each in lt:
        c_list.append(each[0])
    subjects2 = c_list
    for keys, value in Dict.items():
        print(keys, value)
    # lt = course_picked[0]["Course Name"].tolist()
    print(course_picked[0])
    for i in course_picked:
        course_details.append(dropdown_major_eventhandler(i).to_html())
    output=unique_sorted_values_plus_ALL(timetable.Major)
    tt = Dict
    
    global cour1
    cour1 = drop_clash(ccc_courses.drop_duplicates(), lt, tt)
    sub1 = []
    
    print("hello")
    for i in range(len(cour1)):
        if i==0:
            sub1.append(cour1[0])
        elif sub1[len(sub1)-1][1] != cour1[i][1]:
            sub1.append(cour1[i])
    cour1=sub1
    global fin_list2
    for i in range(len(cour1)):
        fin_list2.append(cour1[i][1])
        print(i,cour1[i][1])

    fin_list.clear()
    return render_template('products.html', out=output,my_df=course_details,my_dict=Dict, subjects = c_list, uwe = list_cour,uwe_list = fin_list,ccc=fin_list2)

global cour
global sub  

def check_to_table(each, day, Dict1):
    dic_day = {"M": 0, "T": 1, "W": 2, "F": 4, "S": 5}
    st = each[3]
    end = each[4]
    time_st = '16/4/2020 '+str(st)
    date_format = '%d/%m/%Y %H:%M:%S'
    given_time_st = datetime.strptime(time_st, date_format)
    time_end = '16/4/2020 '+str(end)
    given_time_end = datetime.strptime(time_end, date_format)
    while given_time_st < given_time_end:
        string = str(given_time_st)
        value = Dict1[string[11:]][dic_day[day]]
        if value != " ---- ":
            return 0
        given_time_st += timedelta(minutes=30)
    return each

def drop_clash(uwes, data,Dict2):
#     name_courses(Dict)
    final = []
    uwe = uwes.values.tolist()
    for each in uwe:
        if "M" in each[2]:
            res = check_to_table(each, "M", Dict2)
            if res != 0:
                final.append(res)
        if "T" in each[2]:
            res = check_to_table(each, "T", Dict2)
            if res != 0:
                final.append(res)
        if "W" in each[2]:
            res = check_to_table(each, "W", Dict2)
            if res != 0:
                final.append(res)
        if "F" in each[2]:
            res = check_to_table(each, "F", Dict2)
            if res != 0:
                final.append(res)
        if "S" in each[2]:
            res = check_to_table(each, "S", Dict2)
            if res != 0:
                final.append(res)
    return final

fin_list = []
@app.route('/predict3/<c_name>')
def predict3(c_name):
    
    fin_list.clear()

    output=unique_sorted_values_plus_ALL(timetable.Major)
    
    Uwe_courses = timetable.loc[(timetable['Course Code'].str.contains(c_name, na=False))& (timetable['Component'] == "LEC1") ]

    Uwe_courses = Uwe_courses.iloc[:, [0,1,5,6,7]]
    print(Uwe_courses,"\n\n")
    print(lt2,"\n\n")
    global cour
    cour = drop_clash(Uwe_courses.drop_duplicates(), lt2, tt)
    sub = []
    for i in range(len(cour)):
        if i==0:
            sub.append(cour[0])
        elif sub[len(sub)-1][1] != cour[i][1]:
            sub.append(cour[i])

   
    cour=sub
    for i in range(len(cour)):
        fin_list.append(cour[i][1])
        print(i,cour[i][1])

    print("\n\n")
    return render_template('products.html', out=output,my_dict=tt, subjects = subjects2, uwe = list_cour, uwe_list = fin_list, ccc = fin_list2)

def add_to_table1(data, day, Dict):
    dic_day = {"M": 0, "T": 1, "W": 2, "F": 4, "S": 5}
    st = data[3]
    end = data[4]
    time_st = '16/4/2020 '+str(st)
    date_format = '%d/%m/%Y %H:%M:%S'
    given_time_st = datetime.strptime(time_st, date_format)
    time_end = '16/4/2020 '+str(end)
    given_time_end = datetime.strptime(time_end, date_format)
    while given_time_st < given_time_end:
        string = str(given_time_st)
        Dict[string[11:]].pop(dic_day[day])
        Dict[string[11:]].insert(dic_day[day], data[1])
        if day == "T":
            Dict[string[11:]].pop(dic_day[day] + 2)
            Dict[string[11:]].insert(dic_day[day] + 2, data[1])
        given_time_st += timedelta(minutes=30)

def add_curr(Dict, cour,j):
    lst = [i[1] for i in cour]
    for i in range(len(lst)):
        print(i, lst[i])
    subject = cour[j]
    if "M" in subject[2]:
        add_to_table1(subject, "M", Dict)
    if "T" in subject[2]:
        add_to_table1(subject, "T", Dict)
    if "W" in subject[2]:
        add_to_table1(subject, "W", Dict)
    if "F" in subject[2]:
        add_to_table1(subject, "F", Dict)
    if "S" in subject[2]:
        add_to_table1(subject, "S", Dict)

rem = []
@app.route('/predict4/<c_name>')
def predict4(c_name):
    global rem
    if(c_name[0]=='C' and c_name[1]=='C' and c_name[2]=='C'):
        for i in range(len(cour1)):
            if(c_name==cour1[i][1]):
                subjects2.append(cour1[i][0])
                rem.append(cour1[i][1])
                add_curr(tt,cour1,i)
                break
            print(i,cour[i][1])
    else:

        for i in range(len(cour)):
            if(c_name==cour[i][1]):
                subjects2.append(cour[i][0])
                rem.append(cour[i][1])
                add_curr(tt,cour,i)
                break
            print(i,cour[i][1])
            
        
    print(c_name,"\n\n")
    output=unique_sorted_values_plus_ALL(timetable.Major)
    return render_template('products.html', out=output,my_dict=tt, subjects = subjects2, uwe = list_cour, uwe_list = fin_list, ccc=fin_list2,rem = rem)

# def del_from_table(data, Dict):
#     for key in Dict:
#         value = Dict[key]
#         for i in range(len(value)):
#             if value[i] == data:
#                 value[i] = " ---- "

# def del_curr(Dict):
#     choice = input("Enter which subject you want to delete:")
#     del_from_table(choice, Dict)

@app.route('/predict5/<c_name>')
def predict5(c_name):
    
    for i in range(len(cour1)):
        print(cour1[i][1])
        if(cour1[i][1]==c_name):
            print(subjects2)
            subjects2.remove(cour1[i][0])
    for i in range(len(cour)):
        print(cour[i][1])
        if(cour[i][1]==c_name):
            subjects2.remove(cour[i][0])
    for key in tt:
        value = tt[key]
        for i in range(len(value)):
            if value[i] == c_name:
                value[i] = " ---- "
    rem.remove(c_name)
    output=unique_sorted_values_plus_ALL(timetable.Major)

    return render_template('products.html', out=output,my_dict=tt, subjects = subjects2, uwe = list_cour, uwe_list = fin_list, ccc=fin_list2,rem = rem)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except:
        print("Some Error Occurred, Please go back.")
