from flask import request, Flask, escape, render_template, jsonify
import sqlite3
import pymysql
import requests
import json

type_translate_dict={
    'speed': 'speed',
    'velocity': 'speed',
    'residual_energy': 'soc'
}

# rawDbName = './raw.db'

def parse_position(pos_raw):
    if pos_raw > 200:
        return float(pos_raw)/1000000
    else:
        return float(pos_raw)


def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d 

def getRawAllData():
    conn = sqlite3.connect(rawDbName)
    conn.row_factory = dict_factory
    c = conn.cursor()
    cursor = c.execute("SELECT Id, Time, Text, UserName FROM MENTION")
    result = []
    for row in cursor:
        print(row)
        result.append(row)
    conn.close()
    return result


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % (username)

@app.route('/ht')
def ht():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

# 请求全部车辆位置与状态信息
@app.route('/query/all/location/batch')
def query_all_location():
    db_loc = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    print("/query/all/location/batch")
    cursor_loc = db_loc.cursor()
    cursor_loc.execute("SELECT vin, CAST(create_time AS CHAR) collectTime, create_time, longi_val, lati_val, status, caution_level, caution_flag FROM xmjl_sql WHERE create_time IN (SELECT max(create_time) from xmjl_sql GROUP BY vin);")
    # cursor.execute("SELECT vin, create_time, longi_val, lati_val, status, caution_level, caution_flag FROM xmjl_sql WHERE create_time IN (SELECT max(create_time) from xmjl_sql GROUP BY vin);")
    raw_data_loc = cursor_loc.fetchall()
    # print(raw_data)
    db_loc.close()

    result_data_loc = []
    for item in raw_data_loc:
        result_data_loc.append({
            'VIN': item[0],
            'collectTime': item[1],
            'longitude': item[3],
            'latitude': item[4],
            'status': item[5],
            'caution_level': item[6],
            'caution_flag': item[7]
        })
    # print(result_data)
    return jsonify(result_data_loc)

# 请求全部车辆的vin信息
@app.route('/query/all/vin')
def query_all_vin():
    db_vin = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    print("/query/all/vin")
    cursor_vin = db_vin.cursor()
    cursor_vin.execute("SELECT DISTINCT vin FROM xmjl_sql;")
    # cursor.execute("SELECT vin, create_time, longi_val, lati_val, status, caution_level, caution_flag FROM xmjl_sql WHERE create_time IN (SELECT max(create_time) from xmjl_sql GROUP BY vin);")
    raw_data_vin = cursor_vin.fetchall()
    # print(raw_data_vin)
    db_vin.close()

    result_data_vin = []
    for item in raw_data_vin:
        result_data_vin.append({
            'VIN': item[0],
            # 'collectTime': item[1],
            # 'longitude': item[3],
            # 'latitude': item[4],
            # 'status': item[5],
            # 'caution_level': item[6],
            # 'caution_flag': item[7]
        })
    # print(result_data)
    return jsonify(result_data_vin)

# TODO:再说
@app.route('/query/history/status')
def query_history_status():
    limit = 100
    if (int(request.args.get("limit"))):
        limit = int(request.args.get("limit"))
    print("/query/history/status?limit=%d" % (limit))

@app.route('/query/single/route')
def query_single_route():
    limit = 100
    if (int(request.args.get("limit"))):
        limit = int(request.args.get("limit"))
    car_vin = request.args.get("car_VIN")
    print("/query/history/status?vin=%s&limit=%d" % (car_vin,limit))

    db_single_route = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    cursor_single_route = db_single_route.cursor()

    cursor_single_route.execute("\
        SELECT DISTINCT CAST(create_time AS CHAR) collectTime, longi_val, lati_val FROM xmjl_sql \
        WHERE vin = '%s' and create_time > date_sub(current_timestamp(), interval %d minute) ORDER BY collectTime;" %\
            (car_vin, limit))
    raw_data_single_route = cursor_single_route.fetchall()
    db_single_route.close()

    result_data_single_route = []
    for item in raw_data_single_route:
        result_data_single_route.append({
            'collectTime': item[0],
            'longitude': parse_position(item[1]),
            'latitude': parse_position(item[2]),
        })
    # print(result_data)
    return jsonify(result_data_single_route)

@app.route('/query/single/history')
def query_single_history():
    limit = 100
    if (int(request.args.get("limit"))):
        limit = int(request.args.get("limit"))
    car_vin = request.args.get("car_VIN")
    request_type = request.args.get("type")
    print("/query/history/history?vin=%s&type=%s&limit=%d" % (car_vin,request_type,limit))

    db_single_history = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    cursor_single_history = db_single_history.cursor()

    cursor_single_history.execute("\
        SELECT DISTINCT CAST(create_time AS CHAR) collectTime, %s FROM xmjl_sql \
        WHERE vin = '%s' and create_time > date_sub(current_timestamp(), interval %d minute) ORDER BY collectTime;" %\
            (type_translate_dict[request_type], car_vin, limit))
    raw_data_single_history = cursor_single_history.fetchall()
    db_single_history.close()

    result_data_single_history = []
    for item in raw_data_single_history:
        result_data_single_history.append({
            'collectTime': item[0],
            request_type: item[1],
        })
    # print(result_data)
    return jsonify(result_data_single_history)

@app.route('/query/single/eagle/create')
def single_eagle_create():
    url_single_eagle_create="http://yingyan.baidu.com/api/v3/entity/add"
    request_single_eagle_create = request.args.to_dict()
    print(request_single_eagle_create)
    # request_single_eagle_create['service_id'] = int(request_single_eagle_create['service_id'])
    # headers = {
    #     "Content-Type": "application/json; charset=UTF-8"
    # }

    print(request_single_eagle_create)
    response_single_eagle_create = requests.post(url_single_eagle_create, data=request_single_eagle_create)

    result_single_eagle_create = response_single_eagle_create.text
    print(response_single_eagle_create)

    return jsonify(result_single_eagle_create)


@app.route('/query/single/info_java')
def query_single_infojava():
    car_vin = request.args.get("car_VIN")
    print("/query/single/info_java?vin=%s" % (car_vin))

    db_infojava = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    print("/query/all/location/batch")
    cursor_infojava = db_infojava.cursor()
    cursor_infojava.execute("SELECT vin, CAST(create_time AS CHAR) collectTime, create_time, \
        status, speed, soc, temperature, longi_val, lati_val, \
        caution_level, caution_flag \
        FROM xmjl_sql \
        WHERE vin = '%s' AND create_time IN (SELECT max(create_time) from xmjl_sql WHERE vin = '%s');" \
            % (car_vin, car_vin))
    # cursor.execute("SELECT vin, create_time, longi_val, lati_val, status, caution_level, caution_flag FROM xmjl_sql WHERE create_time IN (SELECT max(create_time) from xmjl_sql GROUP BY vin);")
    raw_data_infojava = cursor_infojava.fetchall()
    # print(raw_data)
    db_infojava.close()

    result_data_infojava = []
    for item in raw_data_infojava:
        result_data_infojava.append({
            'VIN': item[0],
            'collectTime': item[1],
            'status': item[3],
            'speed': item[4],
            'soc': item[5],
            'temperature': item[6],
            'longitude': item[7],
            'latitude': item[8],
            'caution_level': item[9],
            'caution_flag': item[10]
        })
    # print(result_data)
    return jsonify(result_data_infojava)



@app.route('/js')
def js():
    return {
        'name':'1',
        'id':'22',
    }

@app.route('/rawAll')
def rawAll():
    mentionAll = getRawAllData()
    print(mentionAll)
    return jsonify(mentionAll)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8101,
    )
