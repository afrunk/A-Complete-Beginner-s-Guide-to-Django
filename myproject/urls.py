"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path

# 从 boards APP 中导入 views
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 调用views.home
    path('',views.home,name='home'),
    # 分页 为了适配之前的 url 路由适配方法 所以才用 re_path
    # re_path('boards/(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
    # 修改为当前主流的 path 适配方法
    path('boards/<int:pk>/',views.board_topics_2,name='board_topics2'),
    path('boards/<int:pk>/new/',views.new_topic,name='new_topic'),
    path('jsrender',views.jsrender,name='jsrender'), # jsrender 传递参数
]
