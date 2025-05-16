import pandas as pd
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
import datetime
from Food_Recommend import settings
from .models import *
from django.utils.timezone import now
from django.db.models import Count, Sum, Avg

from django.db.models.functions import Cast
from django.db import models

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'})
        User.objects.create(username=username, password=password)
        return JsonResponse({})
    return render(request, 'auth-register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        if username == '' or password == '':
            return JsonResponse({'error': '用户名和密码不能为空'})
        user = User.objects.filter(username=username).first()
        if user is not None and user.password == password:
            # 登录成功，保存用户id到session中
            request.session['user_id'] = user.id
            return JsonResponse({'user_id': user.id})
        else:
            return JsonResponse({'error': '用户名或密码不正确'})
    return render(request, 'auth-login.html')


def index(request):
    total_users = User.objects.count()

    # 统计美食总数
    total_foods = Foods.objects.count()

    # 统计美食类型
    food_type_stats = list(Foods.objects.values('foodtype').annotate(count=Count('id')))

    # 统计平均价格
    avg_price = Foods.objects.aggregate(avg_price=Avg('price'))

    # 获取最新评论
    latest_comments = Comment.objects.order_by('-ctime')[:5]

    # 获取收藏统计，增加美食类型、图片和推荐语
    wishlist_stats = Wishlist.objects.values(
        'food__id',
        'food__foodname',
        'food__foodtype',
        'food__imgurl',
        'food__recommend'
    ).annotate(count=Count('user'))

    # 手动格式化日期为字符串，并按天统计用户注册时间
    user_creation_stats = User.objects.annotate(day=Cast('addtime', models.DateField())).values('day').annotate(count=Count('id')).order_by('day')
    user_creation_stats = [
        {'day': stat['day'].strftime('%Y-%m-%d'), 'count': stat['count']}
        for stat in user_creation_stats
    ]

    # 格式化ECharts数据
    user_data = {
        'total_users': total_users,
        'total_foods': total_foods,
        'avg_price': avg_price['avg_price'],
        'food_type_stats': food_type_stats,
        'user_creation_stats': list(user_creation_stats)
    }

    context = {
        'user_data': user_data,
        'latest_comments': latest_comments,
        'wishlist_stats': wishlist_stats,
    }

    return render(request, 'index.html', context)


def user_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponse("未登录", status=401)

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.addtime = request.POST.get('addtime') or now()
        user.info = request.POST.get('info')

        avatar = request.FILES.get('avatar')
        if avatar:
            static_path = os.path.join(settings.BASE_DIR, 'static', 'image')
            os.makedirs(static_path, exist_ok=True)
            filename = os.path.join(static_path, avatar.name)

            with open(filename, 'wb+') as destination:
                for chunk in avatar.chunks():
                    destination.write(chunk)

            user.face = 'image/' + avatar.name

        user.save()
        return redirect('user_view')

    else:
        from_page = request.GET.get('fp', 1)
        return render(request, 'user_view.html', {'user': user, 'from_page': from_page})


def change_password_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponse("未登录", status=401)

    user = get_object_or_404(User, id=user_id)
    error_message = None  # 用于存储错误信息
    success_message = None  # 用于存储成功信息

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # 校验当前密码是否正确（直接比较明文）
        if current_password != user.password:
            error_message = "当前密码错误"
        # 校验新密码与确认密码是否匹配
        elif new_password != confirm_password:
            error_message = "新密码和确认密码不匹配"
        else:
            user.password = new_password
            user.save()
            success_message = "密码修改成功"  # 设置成功信息
            return render(request, 'change_password.html', {'user': user, 'success_message': success_message})

    return render(request, 'change_password.html', {'user': user, 'error_message': error_message})


def foodlist(request):
    # 获取所有食物条目
    foodlist = Foods.objects.all()

    # 获取所有唯一的 foodtype 进行分类
    foodtypes = Foods.objects.values('foodtype').distinct()

    # 获取筛选参数
    selected_category = request.GET.get('category', 'all')

    # 根据选择的分类过滤数据
    if selected_category != 'all':
        foodlist = foodlist.filter(foodtype=selected_category)

    # 设置每页显示的条数
    items_per_page = 18
    paginator = Paginator(foodlist, items_per_page)

    # 获取当前页码，确保页码是合法的正整数
    page_number = request.GET.get('page', 1)  # 默认第一页
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1  # 如果页码小于1，重置为1
    except ValueError:
        page_number = 1  # 如果页码不是整数，重置为1

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        # 如果页码无效或者超出范围，返回最后一页
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'food-list.html', {
        'page_obj': page_obj,
        'foodtypes': foodtypes,
        'selected_category': selected_category
    })


# 详情页
def detail(request, foodid):
    # 获取当前美食的详情
    foodobj = Foods.objects.get(id=foodid)
    # 根据当前美食的 foodtype 获取相关类型的其他美食，并排除当前查看的美食
    foodtypes = Foods.objects.filter(foodtype=foodobj.foodtype).exclude(id=foodid).order_by('?')[:12]
    # 获取其他 20 个美食（可以根据需求调整排序逻辑）
    foodlist = Foods.objects.all().exclude(id=foodid)[:20]
    # 获取所有评论
    commentlist = Comment.objects.filter(fid=foodid)
    # 检查当前用户是否已收藏该美食
    is_wishlist = False
    user_id = request.session.get('user_id')  # 从session中获取用户ID
    if user_id:
        is_wishlist = Wishlist.objects.filter(user_id=user_id, food=foodobj).exists()

    # 将数据传递给模板
    context = {
        'foodinfo': foodobj,
        'foodlist': foodlist,
        'commentlist': commentlist,
        'foodtypes': foodtypes,
        'is_wishlist': is_wishlist,  # 传递收藏状态
    }
    return render(request, 'fooddetails.html', context)


# 评论
def comment(request, foodid):
    if request.method == 'POST':
        uid = request.session['user_id']
        user = User.objects.get(id=uid)
        realname = user.username
        comment_text = request.POST.get("comment", '')

        commentdata = {
            'uid': uid,
            'fid': foodid,
            'realname': realname,
            'conten': comment_text,
            'ctime': datetime.datetime.now()
        }

        # 实例化并保存评论对象
        commentobj = Comment(**commentdata)
        commentobj.save()

        # 返回 JSON 响应，包含新增评论的数据
        response_data = {
            'status': 'success',
            'realname': realname,
            'comment': comment_text,
            'ctime': commentobj.ctime.strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse(response_data)

    return JsonResponse({'status': 'error'}, status=400)


def add_wishlist(request, foodid):
    if request.method == 'POST':
        # 获取当前用户
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # 检查当前美食是否已被收藏
        foodobj = Foods.objects.get(id=foodid)
        if not Wishlist.objects.filter(user=user, food=foodobj).exists():
            # 如果未收藏，则创建收藏记录
            wishlist_item = Wishlist(user=user, food=foodobj)
            wishlist_item.save()
            return JsonResponse({'status': 'success', 'message': '收藏成功'})

    return JsonResponse({'status': 'error', 'message': '操作失败'}, status=400)


def remove_wishlist(request, foodid):
    if request.method == 'POST':
        # 获取当前用户
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # 查找并删除收藏记录
        foodobj = Foods.objects.get(id=foodid)
        Wishlist.objects.filter(user=user, food=foodobj).delete()
        return JsonResponse({'status': 'success', 'message': '取消收藏成功'})

    return JsonResponse({'status': 'error', 'message': '操作失败'}, status=400)


def food_rec(request):
    user_id = request.session.get('user_id')  # 获取当前登录用户的ID
    if not user_id:
        # 如果用户未登录，则重定向到登录页面
        return redirect('login')

    # 使用外键字段 'food' 进行查询，并优化查询
    recommended_foods = Rec.objects.filter(user_id=user_id).select_related('food')

    # 构建美食的详细信息列表
    food_details = []
    for rec in recommended_foods:
        food = rec.food
        food_details.append({
            'foodname': food.foodname,
            'foodtype': food.foodtype,
            'imgurl': food.imgurl,
            'recommend': food.recommend,
            'id': food.id,
        })

    context = {
        'food_details': food_details,
    }

    return render(request, 'food-rec.html', context)


def keshihua(request):
    author_obj = Fenxi1.objects.all()
    cate_obj = Fenxi2.objects.all()
    comment_obj = Fenxi3.objects.all()
    collect_obj = Fenxi4.objects.all()
    authors = [[], []]
    comment = [[], []]
    collect = [[], []]

    for author_obj_item in author_obj:
        authors[0].append(author_obj_item.author_num)
        authors[1].append(author_obj_item.author_list)

    for comment_obj_item in comment_obj:
        comment[0].append(comment_obj_item.comment_num)
        comment[1].append(comment_obj_item.comment_list)
    for collect_obj_item in collect_obj:
        collect[0].append(collect_obj_item.collect_num)
        collect[1].append(collect_obj_item.collect_list)
    context = {'authors': authors,
               'cate_obj': cate_obj,
               'comment': comment,
               'collect': collect}
    return render(request, 'keshihua.html', context)


def logout(request):
    # 清除session的所有内容
    request.session.flush()
    # 重定向到登录页面
    return redirect('login')


def wordcloud_view(request):
    # 获取请求的类型，默认为'全部'
    food_type = request.GET.get('type', '全部')

    # 根据食品类型进行查询
    if food_type == '全部':
        foods = Fenxi5.objects.all()
    else:
        foods = Fenxi5.objects.filter(foodtype=food_type)

    # 准备词云数据
    data_list = [
        {"name": food.name, "value": food.value}
        for food in foods
    ]

    # 返回一个 JSON 响应
    return JsonResponse({"data": data_list})

def wordcloud_page(request):
    # 获取所有不同的 foodtype，方便前端展示选择项
    food_types = Fenxi5.objects.values_list('foodtype', flat=True).distinct()

    return render(request, 'wordcloud.html', {'food_types': food_types})