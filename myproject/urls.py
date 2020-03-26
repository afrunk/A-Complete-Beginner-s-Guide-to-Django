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
from django.urls import path,re_path,include
from django.contrib.auth import views as auth_views
# 从 boards APP 中导入 views
from boards import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 调用views.home
    path('',views.home,name='home'),
    # 注册
    path('signup/',accounts_views.signup,name='signup'),
    # 登出
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 登录
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    re_path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path(r'settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path(r'settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    # 分页 为了适配之前的 url 路由适配方法 所以才用 re_path
    # re_path('boards/(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
    # 修改为当前主流的 path 适配方法
    path('boards/<int:pk>/',views.board_topics_2,name='board_topics2'),
    path('boards/<int:pk>/new/',views.new_topic,name='new_topic'),
    path('jsrender',views.jsrender,name='jsrender'), # jsrender 传递参数

    # 回复列表路由
    path('boards/<int:pk>/topics/<int:topic_pk>/',views.topic_posts,name='topic_posts'),
    # 添加新的回复
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/',views.reply_topic,name='reply_topic'),

]
