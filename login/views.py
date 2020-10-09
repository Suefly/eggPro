from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# 编写装饰器检查用户是否登录



def check_login(func):
    def inner(request, *args, **kwargs):
        next_url = request.get_full_path()
        # 假设设置的cookie的key为login，value为yes
        if request.get_signed_cookie("login", salt="SSS", default=None) == 'yes':
            # 已经登录的用户，则放行
            return func(request, *args, **kwargs)
        else:
            # 没有登录的用户，跳转到登录页面
            return redirect(f"/login?next={next_url}")

    return inner


# 编写用户登录页面的控制函数
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next_url")
        print('#'*100)
        print('request',request.POST)
        print('#'*100)
        print(username,password,next_url)
        # 对用户进行验证，假设用户名为：aaa, 密码为123
        if username == 'machuang@boyar.cn' and password == '123456':
            # 执行其他逻辑操作，例如保存用户信息到数据库等
            # print(f'next_url={next_url}')
            # 登录成功后跳转,否则直接回到主页面
            if next_url and next_url != "/logout/":
                response = redirect(next_url)
            else:
                response = redirect("/")
            # 若登录成功，则设置cookie，加盐值可自己定义取，这里定义12小时后cookie过期
            response.set_signed_cookie("login", 'yes', salt="SSS", max_age=60*60*12)
            return response
        else:
            # 登录失败，则返回失败提示到登录页面
            error_msg = '登录验证失败，请重新尝试'
            return render(request, "login.html", {
                'login_error_msg': error_msg,
                'next_url': next_url,
            })
    # 用户刚进入登录页面时，获取到跳转链接，并保存
    next_url = request.GET.get("next", '')
    return render(request, "login.html", {
        'next_url': next_url
    })


# 登出页面
def logout(request):
    rep = redirect("/login/")
    # 删除用户浏览器上之前设置的cookie
    rep.delete_cookie('login')
    return rep


# 给主页添加登录权限认证
@check_login
def index(request):
    return render(request, "index.html")
