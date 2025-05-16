import random

import pandas as pd
import pymysql


def chuli():
    data = pd.read_csv('food1.csv', encoding='utf-8')
    print(data.iloc[283]['标题'])
    data = data.drop(data[data['评论数量'] == '川菜'].index)
    data.drop_duplicates(subset=['标题'], keep='first', inplace=True)
    # data['简介']=data['简介'].str.replace(r'\','')
    # data.to_csv('food.csv',index=False)


def run_sql():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='food_recommend',
        charset='utf8'
    )

    cursor = connection.cursor()
    df = pd.read_csv('food.csv', encoding='utf-8')
    print(df.head())

    for i in range(df.shape[0]):
        data = df.iloc[i]
        price_rand = random.uniform(30, 120)
        data1 = (data['标题'], data['类型'], data['简介'], data['图片'], price_rand)
        sql = "insert into myhome_foods(foodname,foodtype,recommend,imgurl,price) values " + str(
            data1) + ";"  # 要与表的机构对其。第一个是主键，自增长的。
        print(sql)
        try:
            cursor.execute(sql)  # 执行sql语句
            connection.commit()  # 连接提交
        except:
            connection.rollback()

    cursor.close()
    connection.close()
    return


def sql2():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='food_recommend',
        charset='utf8'
    )
    cursor = connection.cursor()
    sql = 'select * from myadmin_foods'
    cursor.execute(sql)
    result = cursor.fetchall()
    # for item in result:
    #     print()
    df = pd.read_csv('food1.csv', encoding='utf-8')
    testlist = []
    for item in result:
        testlist.append([item[0], item[1]])
    for i in testlist[1717:]:
        print(i)
        data = df[df['标题'] == i[1]]
        # print(list(data['类型'] == '云南美食')[0])
        # if list(data['类型'] == '云南美食')[0]:
        data2 = (i[0], 12)
        sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
            data2) + ";"
        #     elif list(data['类型'] == '粤菜')[0]:
        #         data2 = (i[0], 38)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        #     elif list(data['类型'] == '湘菜')[0]:
        #         data2 = (i[0], 41)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        #     elif list(data['类型'] == '川菜')[0]:
        #         data2 = (i[0], 42)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        #     elif list(data['类型'] == '西餐')[0]:
        #         data2 = (i[0], 47)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        #     elif list(data['类型'] == '孕婴')[0]:
        #         data2 = (i[0], 45)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        #     else:
        #         data2 = (i[0], 46)
        #         sql1 = "insert into myadmin_foods_typeid(foods_id,foodtype_id) values " + str(
        #             data2) + ";"
        cursor.execute(sql1)
        connection.commit()
    cursor.close()
    connection.close()


run_sql()
# sql2()
