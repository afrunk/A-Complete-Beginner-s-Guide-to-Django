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

# 引入我们创建的表单
from .forms import NewTopicForm
# 新建 topic 的函数
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    user = User.objects.first()

    if request.method =='POST':
        # 如果是 POST 请求 则将请求传入表单
        form = NewTopicForm(request.POST)
        # 如果表单的请求是有效的 则使用 form.save() 存入数据库
        if form.is_valid():
            # save方法返回的一个存入数据库的 Model 实例
            # 因为这是一个 Topic form 所以会创建一个 Topic
            topic = form.save(commit=False)
            topic.board=board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by=user
            )
            # 重定向
            return redirect('board_topics2',pk=board.pk)
    else:
        form = NewTopicForm()
    # 如果数据是无效的 ，django 会给 form 添加错误列表
    # 然后 视图函数不会做任何处理并且原本的表单页面 并显示错误
    return render(request,'new_topic.html',{'board':board,'form':form})