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

from django.db.models import Count
# re 匹配方法
def board_topics(request,pk):
    #pk 表示主键的意思
    board = Board.objects.get(pk=pk)
    # 回复数 直接使用 sql 语句实现回复数的统计
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request,'topics.html',{'board':board,'topics':topics})

# 适配 django2.2 的路由 path 匹配算法
def board_topics_2(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request, 'topics.html', {'board': board})

# 引入我们创建的表单
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required
# 避免它被未登录的用户访问
@login_required
# 新建 topic 的函数
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    if request.method =='POST':
        # 如果是 POST 请求 则将请求传入表单
        form = NewTopicForm(request.POST)
        # 如果表单的请求是有效的 则使用 form.save() 存入数据库
        if form.is_valid():
            # save方法返回的一个存入数据库的 Model 实例
            # 因为这是一个 Topic form 所以会创建一个 Topic
            topic = form.save(commit=False)
            topic.board=board
            topic.starter = request.user # <- hrer
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by=request.user # and here
            )
            # 重定向
            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    # 如果数据是无效的 ，django 会给 form 添加错误列表
    # 然后 视图函数不会做任何处理并且原本的表单页面 并显示错误
    return render(request,'new_topic.html',{'board':board,'form':form})

# 回复列表
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    # 尝试使用外键的反方向操作来读取 post 里面的内容
    for post in topic.post_set.all():
        print(post.message)
    topic.views +=1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

# 添加回复
# 防止未登录的用户进行添加
from .forms import PostForm
@login_required
def reply_topic(request,pk,topic_pk):
    # 获取 topic 的内容
    topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts',pk=pk,topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})