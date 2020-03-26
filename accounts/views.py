from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
# 传入新的表单
from .forms import SingUpForm


def signup(request):
    if request.method=='POST':
        # 对表单进行赋值
        form = SingUpForm(request.POST)
        # 判断表单是否合适
        if form.is_valid():
            # 存储数据
            user = form.save()
            # 手动验证数据是否合适
            auth_login(request,user)
            # 重定向到首页
            return redirect('home')
    else:
        form = SingUpForm()
    # 如果不成功则跳转回原页面
    return render(request, 'signup.html', {'form':form})