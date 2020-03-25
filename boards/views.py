from django.shortcuts import render,get_object_or_404,redirect
# 导入 HttpResponse 对象 由 DJango 自动创建
from django.http import HttpResponse,JsonResponse
# 导入时间模块
import datetime
# 导入 Board 为数据调用做准备
from .models import Board,Topic,Post
import json

from django.contrib.auth.models import  User

# Create your views here.
# 首页的视图函数
def home(request):
    boards = Board.objects.all()# 从数据库中读取 board 表内的数据
    return render(request,'home.html',{'boards':boards})

# render 传递参数至 js,HTML 调用 js 函数展示
def jsrender(request):
    list = ['HTML','Python', 'Json', 'JS']
    return render(request, 'jsRender.html', {
        'List': json.dumps(list),
    })

# re 匹配方法
def board_topics(request,pk):
    #pk 表示主键的意思
    board = Board.objects.get(pk=pk)
    return render(request,'topics.html',{'board':board})

# 适配 django2.2 的路由 path 匹配算法
def board_topics_2(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request, 'topics.html', {'board': board})

# 新建 topic 的函数
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)

    if request.method =='POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first() # 临时使用一个账号作为登录用户

        topic = Topic.objects.create(
            subject = subject,
            board = board,
            starter= user
        )

        post = Post.objects.create(
            message = message,
            topic = topic,
            created_by=user
        )
        # 重定向
        return redirect('board_topics2',pk=board.pk)
    return render(request,'new_topic.html',{'board':board})