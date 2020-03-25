from django.db import models
# 我们不构建用户模型 直接继承 Django 内置模块
from django.contrib.auth.models import User
# Create your models here.

'''
为什么每个类都需要继承 models.Model 
因为所有的模型都是 django.db.models.Field 子类 
这样每个类都被转换为数据库内的表

每个字段由 django.db.models.Field子类的实例表示
它们并将会被转换为数据库的列
字段 CharField、DataTimeField等等
都是 django.db.models.Filed的子类

有些字段需要参数 例如 CharField 
我们应该设定一个 max_length 这些信息将用于创建数据库列 
Django 需要知道数据库列需要多大
该 max_length 参数也将被 Django Forms API 用来验证用户输入

related_name 是可选项
但是如果我们不为它设置一个名称
Django会自动生成它：（class_name)_set
如在 Board 模型中，所有的 Topic 列表将用 topic_set 属性表示
如果设置 related_name ='+' 
指示 Django 我们不需要这种反向关系，所以它会被忽略
也就是说我们不需要关系用户修改哪些帖子
'''

# 模块
class Board(models.Model):
    # unique= True 强调数据库级别字段的唯一性
    # 必须添加 default 否则会报错告诉你必须添加默认值
    name = models.CharField(max_length=30,unique=True,default='test')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 帖子
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now_add=True)
    # Board 可以通过 related_name 参数用于创建反向关系
    # 访问属于该板块下的 Topic 列表
    board =models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
    starter= models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)

# 回复
class Post(models.Model):
    message = models.TextField(max_length=4000)
    #模型之间创建一个链接，并在数据库级别创建适当的关系
    # 参数 related_name ,用于引用它关联的模型
    # 比如在 Topic 中可以使用 Topic.posts来查看这个帖子有哪些回复
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    # auto_now_add 自动添加当前日期和时间
    created_at = models.DateTimeField(auto_now_add=True)
    # null= True 表示空值也将会被存储
    update_at = models.DateTimeField(null=True)
    # 在 User 中可以使用 User.posts 来查看这个用户有哪些回复
    created_by = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    # 看注释理解 related_name = '+' 的用法
    update_by = models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)