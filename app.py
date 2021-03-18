from flask import Flask, escape, render_template, jsonify
import sqlite3
import pymysql

# rawDbName = './raw.db'


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

@app.route('/query/all/vin')
def query_all_vin():
    db_vin = pymysql.connect(host="localhost",user="root",passwd="sjtu123",db="xmjl")
    print("/query/all/vin")
    cursor_vin = db_vin.cursor()
    cursor_vin.execute("SELECT DISTINCT vin FROM xmjl_sql;")
    # cursor.execute("SELECT vin, create_time, longi_val, lati_val, status, caution_level, caution_flag FROM xmjl_sql WHERE create_time IN (SELECT max(create_time) from xmjl_sql GROUP BY vin);")
    raw_data_vin = cursor_vin.fetchall()
    print(raw_data_vin)
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
