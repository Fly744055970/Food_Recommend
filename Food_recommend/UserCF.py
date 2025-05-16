# coding = utf-8

# 基于用户的协同过滤推荐算法实现
import csv
import random
import pymysql
import math
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的3个用户，为其推荐3部美食
        self.n_sim_user = 3
        self.n_rec_food = 5

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.food_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded food number = %d' % self.n_rec_food)


    # 读文件得到“用户-美食”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, food, rating = line.split(',')
            # if random.random() < pivot:
            self.trainSet.setdefault(user, {})
            self.trainSet[user][food] = rating
            trainSet_len += 1
            # else:
            #     self.testSet.setdefault(user, {})
            #     self.testSet[user][food] = rating
            #     testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)


    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)


    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“美食-用户”倒排索引
        # key = foodID, value = list of userIDs who have seen this food
        print('Building food-user table ...')
        food_user = {}
        for user, foods in self.trainSet.items():
            for food in foods:
                if food not in food_user:
                    food_user[food] = set()
                food_user[food].add(user)
        print('Build food-user table success!')

        self.food_count = len(food_user)
        print('Total food number = %d' % self.food_count)

        print('Build user co-rated foods matrix ...')
        for food, users in food_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated foods matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')


    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_food
        rank = {}
        watched_foods = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for food in self.trainSet[v]:
                if food in watched_foods:
                    continue
                rank.setdefault(food, 0)
                rank[food] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]


    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_food
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_foods = set()

        # 打开数据库连接
        db = pymysql.connect(host='localhost', user='root', password='123456', database='food_recommend', charset='utf8')
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        sql1 = "truncate table myhome_rec;"
        cursor.execute(sql1)
        db.commit()
        sql = "insert into myhome_rec(user_id,food_id,score ) values (%s,%s,%s)"

        for i, user, in enumerate(self.trainSet):
            test_foods = self.testSet.get(user, {})
            rec_foods = self.recommend(user)
            print(user,rec_foods)
            for item in rec_foods:
                data=(user,item[0],item[1])
                cursor.execute(sql, data)
            db.commit()
            #rec_foods 是推荐后的数据
            #把user-rec-rating 存到数据库
            for food, w in rec_foods:
                if food in test_foods:
                    hit += 1
                all_rec_foods.add(food)
            rec_count += N
            test_count += len(test_foods)

        cursor.close()
        db.close()



if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='123456', database='food_recommend', charset='utf8')
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询

    sql = "select * from myhome_wishlist"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    with open('rating.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id','food_id','rating'])
        for item in data:
            writer.writerow([item[3], item[2],1])

    rating_file = 'rating.csv'
    userCF = UserBasedCF()
    userCF.get_dataset(rating_file)
    userCF.calc_user_sim()
    userCF.evaluate()
