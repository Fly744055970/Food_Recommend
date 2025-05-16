from django.db import models
from datetime import datetime


# Create your models here.
class User(models.Model):
    """ 用户表 """
    username = models.CharField(max_length=255, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(unique=True, max_length=100)
    # 手机号
    phone = models.CharField(unique=True, max_length=11)
    # 个性简介
    info = models.TextField(blank=True, null=True)
    # 头像
    face = models.CharField(max_length=255, unique=True, blank=True, null=True)
    # 注册时间
    addtime = models.DateTimeField(default=datetime.now(), db_index=True)

    class Meta:
        # 表名
        # managed = False
        db_table = 'users'


# 菜品类
class Foods(models.Model):
    foodname = models.CharField(max_length=70)  # 菜品名称
    foodtype = models.CharField(max_length=20)  # 菜品类型
    recommend = models.CharField(max_length=255, null=True)  # 推荐语
    # price = models.DecimalField(max_digits=5, decimal_places=2)  # 价格
    # num = models.IntegerField()  # 库存
    # fooddetail = models.TextField(null=True)  # 商品详情
    # cate = models.CharField(max_length=1, default='0')  # 0上架 1热卖 2促销  3推荐 4下架
    # isdel = models.CharField(max_length=6, default="004001")  # 是否逻辑删除  004001可用  004002不可用
    # isspider = models.IntegerField(default=0)  # 库存
    imgurl = models.CharField(max_length=255)  # 图片
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Comment(models.Model):
    uid = models.IntegerField()
    fid = models.IntegerField()
    realname = models.CharField(max_length=11)
    conten = models.TextField()
    ctime = models.DateTimeField(null=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户外键
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)  # 美食外键
    added_time = models.DateTimeField(auto_now_add=True)  # 添加收藏的时间

    class Meta:
        unique_together = ('user', 'food')

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.food.foodname}"

class Rec(models.Model):
    #用户ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户外键
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    score=models.DecimalField(max_digits=5,decimal_places=2)#菜品商品的数量


class Fenxi1(models.Model):
    author_num = models.IntegerField()  #
    author_list = models.CharField(max_length=50)  #


class Fenxi2(models.Model):
    cates_num = models.IntegerField()  #
    cates_list = models.CharField(max_length=50)  #


class Fenxi3(models.Model):
    comment_num = models.IntegerField()  #
    comment_list = models.CharField(max_length=50)  #


class Fenxi4(models.Model):
    collect_num = models.IntegerField()  #
    collect_list = models.CharField(max_length=50)

class Fenxi5(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    foodtype = models.CharField(max_length=20)

