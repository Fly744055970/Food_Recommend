import random
import re
import jieba
import string
from collections import Counter
import pandas as pd
import pymysql
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='food_recommend',
        charset='utf8'
    )

cursor = connection.cursor()


def run_sql():

    df=pd.read_csv('food.csv',encoding='utf-8')
    print(df.head())

    authors_num = list(df['作者'].value_counts())[:20]
    authors_list = list(df['作者'].value_counts().index)[:20]

    cates_num = list(df['类型'].value_counts())
    cates_list = list(df['类型'].value_counts().index)

    comment_num = list(df.sort_values(by='评论数量',ascending=False)['评论数量'])[:20]
    comment_list =list(df.sort_values(by='评论数量',ascending=False)['标题'])[:20]

    collect_num = list(df.sort_values(by='收藏数量',ascending=False)['收藏数量'])[:20]
    collect_list =list(df.sort_values(by='收藏数量',ascending=False)['标题'])[:20]
    print(comment_list,comment_num,cates_list,cates_num)
    for i in range(len(authors_num)):

        data1=(collect_num[i],collect_list[i])
        sql = "insert into myhome_fenxi4(collect_num,collect_list) values " + str(data1) + ";"
        print(sql)
        try:
            cursor.execute(sql)  #执行sql语句
            connection.commit() #连接提交
        except:
            connection.rollback()
    for i in range(len(authors_num)):

        data1=(authors_num[i],authors_list[i])
        sql = "insert into myhome_fenxi1(author_num,author_list) values " + str(data1) + ";"
        print(sql)
        try:
            cursor.execute(sql)  #执行sql语句
            connection.commit() #连接提交
        except:
            connection.rollback()
    for i in range(len(cates_num)):

        data1=(cates_num[i],cates_list[i])
        sql = "insert into myhome_fenxi2(cates_num,cates_list) values " + str(data1) + ";"
        print(sql)
        try:
            cursor.execute(sql)  #执行sql语句
            connection.commit() #连接提交
        except:
            connection.rollback()
    for i in range(len(comment_list)):

        data1=(comment_list[i],comment_num[i])
        sql = "insert into myhome_fenxi3(comment_list,comment_num) values " + str(data1) + ";"
        print(sql)
        try:
            cursor.execute(sql)  #执行sql语句
            connection.commit() #连接提交
        except:
            connection.rollback()
    cursor.close()
    connection.close()
    return


def remove_unsupported_chars(text):
    # 移除表情符号等非标准字符
    return re.sub(r'[^\w\u4e00-\u9fff]+', '', text)

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f)
    return stopwords


def fenxi5():
    # 加载数据
    df = pd.read_csv('food.csv')
    df['简介'] = df['简介'].fillna('')
    text = ' '.join(df['简介'])

    # 加载停用词表
    stopwords = load_stopwords('cutword.txt')

    # 移除标点符号
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    text = text.replace(' ', '')

    # 分词
    words = jieba.cut(text)

    # 过滤停用词
    words = [word for word in words if word not in stopwords]

    # 统计词频
    word_counts = Counter(words)
    word_counts_df = pd.DataFrame(word_counts.items(), columns=['词语', '出现次数'])
    word_counts_df = word_counts_df.sort_values(by='出现次数', ascending=False)

    # 获取食品类型
    foodtypes = df['类型'].tolist()

    sql = 'insert into myhome_fenxi5(name, value, foodtype) values(%s, %s, %s)'

    for index, row in word_counts_df.iterrows():
        foodtype = foodtypes[index % len(foodtypes)]
        # 移除特殊字符
        word = remove_unsupported_chars(row['词语'])

        # 插入时处理异常
        try:
            cursor.execute(sql, (word, row['出现次数'], foodtype))
        except pymysql.err.DataError as e:
            continue

    connection.commit()


# run_sql()
fenxi5()