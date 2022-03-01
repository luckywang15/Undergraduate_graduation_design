from django.shortcuts import render, redirect
from comments.models import Comments_Board
from django.core.paginator import Paginator

# Create your views here.
def show_comments(request):
    '''评论留言板'''
    # 判断请求是否是GET：
    if request.method == "GET":
        # 从数据库查找数据返回前端
        db = Comments_Board.objects.all()
        limit = 11
        paginator = Paginator(db, limit)  # 按每页10条分页
        page = request.GET.get('page', '1')  # 默认跳转到第一页
        result = paginator.page(page)
        # 返回模板
        return render(request, "comments_board.html", {"data": result})

    # 判断请求是否是POST：
    elif request.method == "POST":
        # 接收前端传送的参数
        name = request.POST.get("name")
        content = request.POST.get("content")

        # 判断接收数据是否为空
        if name != "" and content != "":
            # 连接数据库
            db = Comments_Board()
            # 将数据存入数据库中
            db.name = name
            db.content = content
            # 保存数据
            db.save()
            # 返回到留言板
            return redirect("/comments/")

        else:
            return render(request, "comments_board.html", {"error":"留言内容不能为空"})
    # 如果请求不符合规定则返回主页
    else:
        return redirect("/")