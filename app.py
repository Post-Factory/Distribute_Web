import flask
# import sqlalchemy.sql.expression
from flask import Flask, render_template, Response
from flask import Flask, url_for, render_template, request, redirect, session

import os
from importlib import import_module
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import time
import datetime
import sys
from flask import Flask, render_template

import sqlalchemy
import sqlalchemy as db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import random

import pymysql
pymysql.install_as_MySQLdb()

from PIL import Image
import base64
from io import BytesIO

buffer = BytesIO()

import socket

import pandas as pd

# db 연동
engine = create_engine("mysql://new:new@3.20.99.214:3306/loading_DB")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# db Base 클래스 생성 => DB를 가져올 class를 생성함
Base = declarative_base()
Base.query = db_session.query_property()

# DB 가져오기
connection = engine.connect()
metadata = Base.metadata
metadata.create_all(engine)

def change_DB() :
    schedule_table = db.Table('SCHEDULE', metadata, autoload=True, autoload_with=engine)
    db_session.query(schedule_table).delete()
    db_session.commit()

    storage_table = db.Table('STORAGE', metadata, autoload=True, autoload_with=engine)
    db_session.query(storage_table).delete()
    db_session.commit()

    cargo_table = db.Table('CARGO', metadata, autoload=True, autoload_with=engine)
    db_session.query(cargo_table).delete()
    db_session.commit()

    car_num0 = {'K' : '한국'}
    car_num1 = {'M' : '현대자동차'}
    car_num2 = {'H' : '승용차', 'J' : '승합차', 'F' : '화물', 'M' : '산타페', 'T' : '제네시스'}
    car_num3 = {'J' : ['tussan'], 'K' : ['kona'], 'E' : ['sonata'], 'Z' : ['porter2'], 'S' : ['santafe'], 'D' : ['avante', 'i30'],
                'T' : ['veloster'], 'R' : ['palisade', 'venue'], 'G' : ['G70', 'G80','G90'], 'H' : ['GV80'], 'W' : ['starex'], 'C' : ['ioniq'], 'J':['nexo']}
    car_num4 = {'2' : ['santafe', 'palisade', 'G90'],'T':'tussan', '5' : ['tussan', 'G70'], 'M' : 'G80', 'L':'G80', 'R' :'G80' , 'C':'i30'}
    car_num5 = {'4' : '문4개' , '8' : 'SUV', '3' : '문3개'}
    car_num6 = {'1' : ['일반차량'], '7' : ['스타렉스','포터'], '8' : ['메가트럭', '버스']}
    car_num7 = {'2':'','3':'','5':'','B':'','C':'','D':'','E':'','F':'','G':'','H':'','L':'','N':'','S':'','V':'','M':''}
    car_num8 = {'0':'','1':'','2':'','3':'','4':'','5':'','6':'','7':'','8':'','9':'','x':''}
    car_num9 = {'A' : '2010년식', 'B' :'2011년식', 'C' : '2012년식', 'D' : '2013년식', 'E' :'2014년식', 'F' :'2015년식','G' : '2016년식', 'H' : '2017년식',
                'J':'2018년식', 'K': '2019년식', 'L' : '2020년식', 'M' : '2021년식', 'N' : '2022년식', 'P' :'2023년식', 'Q' : '2024년식'}
    car_num10 = {'U' : 'ULSAN'}

    def vin_decoder(car_vin):
        decode_list = []
        if car_vin[0] in car_num0.keys():
            decode_list.append(car_num0[car_vin[0]])
        if car_vin[1] in car_num1.keys():
            decode_list.append(car_num1[car_vin[1]])
        if car_vin[2] in car_num2.keys():
            decode_list.append(car_num2[car_vin[2]])
        if car_vin[3] in car_num3.keys():
            decode_list.append(car_num3[car_vin[3]])
            if type(car_num3[car_vin[3]]) == list:
                if car_vin[4] in car_num4.keys():
                    try :
                        car = set([car_num4[car_vin[4]]]).intersection(set(car_num3[car_vin[3]]))
                    except :
                        car = set(car_num3[car_vin[3]]).intersection(list(car_num4[car_vin[4]]))
                    try :
                        decode_list.append(list(car)[0])
                    except :
                        num = random.randrange(len(car_num3[car_vin[3]]))
                        decode_list.append(car_num3[car_vin[3]][num])
        if car_vin[5] in car_num5.keys():
            decode_list.append(car_num5[car_vin[5]])
        if car_vin[6] in car_num6.keys():
            decode_list.append(car_num6[car_vin[6]])
        if car_vin[7] in car_num7.keys():
            decode_list.append(car_num7[car_vin[7]])
        if car_vin[8] in car_num8.keys():
            decode_list.append(car_num8[car_vin[8]])
        if car_vin[9] in car_num9.keys():
            decode_list.append(car_num9[car_vin[9]])
        if car_vin[10] in car_num10.keys():
            decode_list.append(car_num10[car_vin[10]])
        return decode_list

    import random

    position = [car_num0, car_num1, car_num2, car_num3, car_num4, car_num5, car_num6, car_num7, car_num8, car_num9,
                car_num10]
    car_vin_list = []

    for i in range(1000):
        car_vin = ''
        for i in range(17):
            if i < 11:
                num = random.randrange(len(position[i].keys()))
                car_vin += list(position[i].keys())[num]
            else:
                num = random.randrange(10)
                car_vin += str(num)

        car_vin_list.append(car_vin)

    storage_car = car_vin_list[:800]
    cargo_car = car_vin_list[800:]

    # STORAGE INSERT
    print("Storage insert Start")
    import random
    import pandas as pd

    phonenums = ['71646177', '76177745', '22433324', '40598151', '77510957', '35106585']

    ip = []
    for i in range(6):
        ip_address = str(random.randrange(256)) + '.' + str(random.randrange(256)) + '.' + str(
            random.randrange(256)) + '.' + str(random.randrange(256))
        ip.append(ip_address)

    inspect_time = []
    now = time.localtime()

    for i in range(80):
        temp_time = str(now.tm_year) + '-'+str(now.tm_mon) + '-' + str(random.randrange(1, now.tm_mday)) + ' ' + str(random.randrange(now.tm_hour)) + ':' + str(random.randrange(now.tm_min)) + ':00'
        inspect_time.append(temp_time)

    storage_data = {'CARGO_VIN': [], 'CARGO_NAME': [], 'INSPECT_TIME': [], 'IP': [], 'LI_PHONENUM': []}
    for i in storage_car:
        cargoname = vin_decoder(i)
        #     print(cargoname[4])

        storage_data['CARGO_VIN'].append(i)
        storage_data['CARGO_NAME'].append(cargoname[4])
        storage_data['INSPECT_TIME'].append(inspect_time[random.randrange(len(inspect_time))])
        storage_data['IP'].append(ip[random.randrange(len(ip))])
        storage_data['LI_PHONENUM'].append(phonenums[random.randrange(len(phonenums))])

    storage_df = pd.DataFrame(storage_data)

    import pymysql
    pymysql.install_as_MySQLdb()

    storage_df.to_sql(name='STORAGE',con=engine, if_exists='append',index=False)
    print("Storage insert End")

    # CARGO INSERT
    print("Cargo insert Start")
    import random
    import pandas as pd

    import sqlalchemy
    from sqlalchemy import text

    phonenums = ['71646177', '76177745', '22433324', '40598151', '77510957', '35106585']

    ip = []
    for i in range(6):
        ip_address = str(random.randrange(256)) + '.' + str(random.randrange(256)) + '.' + str(
            random.randrange(256)) + '.' + str(random.randrange(256))
        ip.append(ip_address)

    now = time.localtime()
    for i in range(80):
        temp_time = str(now.tm_year) + '-'+str(now.tm_mon) + '-' + str(random.randrange(1, now.tm_mday)) + ' ' + str(random.randrange(now.tm_hour)) + ':' + str(random.randrange(now.tm_min)) + ':00'
        inspect_time.append(temp_time)

    vessel_name = ['GLOVIS PRIME', 'GLOVIS SIGMA']

    cargo_data = {'CARGO_VIN': [], 'VESSEL_NAME': [], 'CARGO_NAME': [], 'CARGO_WEIGHT': [], 'CARGO_INSPECT_TIME': [],'IP': [], 'LI_PHONENUM': [], 'DECK': [], 'HOLD': []}

    for i in cargo_car:
        cargoname = vin_decoder(i)
        #     print(cargoname[4])

        car_table = sqlalchemy.Table('CAR', metadata, autoload=True, autoload_with=engine)
        cargo_weight = db_session.query(car_table).filter(text("CAR_NAME=:car_name")).params(car_name=cargoname[4]).all()[0][1]

        cargo_data['CARGO_VIN'].append(i)
        cargo_data['VESSEL_NAME'].append(vessel_name[random.randrange(len(vessel_name))])
        cargo_data['CARGO_NAME'].append(cargoname[4])
        cargo_data['CARGO_WEIGHT'].append(cargo_weight)
        cargo_data['CARGO_INSPECT_TIME'].append(inspect_time[random.randrange(len(inspect_time))])
        cargo_data['IP'].append(ip[random.randrange(len(ip))])
        cargo_data['LI_PHONENUM'].append(phonenums[random.randrange(len(phonenums))])
        cargo_data['DECK'].append(random.randrange(1, 12))
        cargo_data['HOLD'].append(random.randrange(1, 5))

    cargo_df = pd.DataFrame(cargo_data)

    cargo_df.to_sql(name='CARGO',con=engine, if_exists='append',index=False)
    print("Cargo Insert End")

    # INSERT SCHEDULE
    print("SCHEDULE insert Start")
    now = time.localtime()
    import_time = str(now.tm_year) + '-' + str(now.tm_mon) + '-' + str(now.tm_mday) + ' ' + str(now.tm_hour) + ':' + str(now.tm_min) + ':00'
    if (int(now.tm_hour) + 12) >= 24:
        hour = (int(now.tm_hour) + 12) - 24
        export_time = str(now.tm_year) + '-' + str(now.tm_mon) + '-' + str(int(now.tm_mday)+1) + ' ' + str(hour) + ':' + str(now.tm_min) + ':00'
    else :
        export_time = str(now.tm_year) + '-' + str(now.tm_mon) + '-' + str(now.tm_mday) + ' ' + str(int(now.tm_hour)+12) + ':' + str(now.tm_min) + ':00'
    vessel_name = 'GLOVIS PRIME'
    schedule_ton = 400

    print(import_time, export_time, vessel_name, schedule_ton)
    schedule_table = db.Table('SCHEDULE', metadata, autoload=True, autoload_with=engine)
    query = db.insert(schedule_table).values(SCHEDULE_IMPORT=import_time, SCHEDULE_EXPORT=export_time, VESSEL_NAME=vessel_name, SCHEDULE_TON=schedule_ton)
    result_proxy = connection.execute(query)
    result_proxy.close()
    print("SCHEDULE insert End")

app = Flask(__name__)

#실시간 정보공유 페이지
@app.route('/')
def total():
    date = datetime.datetime
    # print(date.now())
    try :
        schedule_table = sqlalchemy.Table('SCHEDULE', metadata, autoload=True, autoload_with=engine)
        import_time = db_session.query(schedule_table).all()[0][0]
        export_time = db_session.query(schedule_table).all()[0][1]

        # print(import_time, export_time)

        if date.now() < import_time or date.now() > export_time :
            # print("if문")
            change_DB()
            time.sleep(2)
    except :
        # print("except")
        change_DB()
        time.sleep(2)

    # schedule_table = sqlalchemy.Table('SCHEDULE', metadata, autoload=True, autoload_with=engine)
    # import_time = db_session.query(schedule_table).all()[0][0]
    # export_time = db_session.query(schedule_table).all()[0][1]
    # # print(import_time, export_time)
    worker_table = sqlalchemy.Table('WORKER', metadata, autoload=True, autoload_with=engine)

    try :
        checker = db_session.query(worker_table).filter(text("WORKER_TASK='checker'")).all()[0][-1]
        driver = db_session.query(worker_table).filter(text("WORKER_TASK='drive'")).all()[0][-1]
        lashing = db_session.query(worker_table).filter(text("WORKER_TASK='lashing'")).all()[0][-1]

    except :
        checker = 0
        driver = 0
        lashing = 0

    cargo_table = sqlalchemy.Table('CARGO', metadata, autoload=True, autoload_with=engine)
    data = db_session.query(cargo_table).order_by(text("CARGO_INSPECT_TIME desc")).all()[:6]
    # print(data)

    date = datetime.datetime

    deck = []
    for i in range(1, 12) :
        percent = (len(db_session.query(cargo_table).filter(text("DECK=:deck_num")).params(deck_num=i).all()) / 100) * 100
        deck.append(percent)

    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    total_num = len(db_session.query(cargo_table).filter(text("IP=:ip")).params(ip=ip).all())

    schedule_table = sqlalchemy.Table('SCHEDULE', metadata, autoload=True, autoload_with=engine)
    # print(deck)
    try :
        import_time = []
        export_time = []
        vessel_name = []
        schedule_list = db_session.query(schedule_table).filter(text("SCHEDULE_EXPORT>=:date")).filter(text("SCHEDULE_IMPORT<=:date")).params(date=date.now()).order_by(text("SCHEDULE_EXPORT")).all()
        for i in schedule_list :
            import_time.append(i[0])
            export_time.append(i[1])
            vessel_name.append(i[2])

        # print(schedule_list)

        limit_time = export_time[0] - date.now()
        # print(limit_time)

        hour, minute, second = str(limit_time).split(':')
        # print(hour, minute, second)
        return render_template('total.html', checker=checker,driver=driver,lashing=lashing,data=data,hour=hour,minute=minute,second=second,vessel_name=vessel_name,deck=deck,total_num=total_num,date=datetime.date.today())
    
    except :
        # print("except")
        hour, minute, second = 0, 0, 0
        return render_template('total.html', checker=checker,driver=driver,lashing=lashing,data=data,hour=hour,minute=minute,second=second,vessel_name=vessel_name,deck=deck,total_num=total_num, date=datetime.date.today())

@app.route('/hol_dec_send', methods=['GET','POST'])
def hol_dec_send() :
    if request.method == 'POST' :
        # # print("post")
        #
        # hold = request.form['hold']
        # deck = request.form['deck']
        #
        # login_table = db.Table('LOGIN', metadata, autoload=True, autoload_with=engine)
        # ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        # db_session.query(login_table).filter(text("IP=:ip")).params(ip=ip).update({'DECK':deck, 'HOLD':hold}, synchronize_session=False)
        # db_session.commit()

        return flask.redirect(flask.url_for('total'))

    else :
        return flask.redirect(flask.url_for('total'))

@app.route('/vessel_send', methods=['GET','POST'])
def vessel_send() :
    if request.method == 'POST' :
        # # print("post")
        #
        # vessel_name = request.form['vessel']
        #
        # login_table = db.Table('LOGIN', metadata, autoload=True, autoload_with=engine)
        # ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        # db_session.query(login_table).filter(text("IP=:ip")).params(ip=ip).update({'VESSEL_NAME':vessel_name}, synchronize_session=False)
        # db_session.commit()

        return flask.redirect(flask.url_for('total'))

    else :
        return flask.redirect(flask.url_for('total'))

@app.route('/worker_send', methods=['GET', 'POST'])
def worker_send() :
    worker_table = db.Table('WORKER', metadata, autoload=True, autoload_with=engine)
    db_session.query(worker_table).delete()
    db_session.commit()

    checker_task = 'checker'
    drive_task = 'drive'
    lashing_task = 'lashing'

    if request.method == 'POST' :
        # print("post")

        checker = request.form['checker']
        drive = request.form['driver']
        lashing = request.form['lashing']

        now = time.localtime()
        today = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        # print(checker, drive, lashing)
        try :
            worker_table = db.Table('WORKER', metadata, autoload=True, autoload_with=engine)
            query = db.insert(worker_table).values(WORKER_TASK=checker_task, WORKER_DATE=today, WORKER_PERSONNEL=checker)
            result_proxy = connection.execute(query)
            result_proxy.close()

            query = db.insert(worker_table).values(WORKER_TASK=drive_task, WORKER_DATE=today,WORKER_PERSONNEL=drive)
            result_proxy = connection.execute(query)
            result_proxy.close()

            query = db.insert(worker_table).values(WORKER_TASK=lashing_task, WORKER_DATE=today,WORKER_PERSONNEL=lashing)
            result_proxy = connection.execute(query)
            result_proxy.close()

            return flask.redirect(flask.url_for('total'))

        except :
            return flask.redirect(flask.url_for('worker'))

    else :
        return flask.redirect(flask.url_for('worker'))

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/worker')
def worker():
    return render_template('worker.html')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=4997, debug=True)
    app.run('localhost', 4997, debug=True)