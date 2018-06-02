from django.shortcuts import render
from accounts.models import Resume


# 사료 구매 / 고기 구매
def main(request):
    return render(request, "main.html")


# 사료 종류 보는 페이지
def feed(request):
    return render(request, "feed.html")


# 고기 구매하는 페이지
def meat(request):
    return render(request, "meat.html")


# 사료 구매(옥수수)하는 페이지
def feed_1(request):
    resume = Resume.objects.get(user=request.user)
    return render(request, "feed_1.html", {
        "card": resume.card,
    })


# 사료 구매(쌀겨)하는 페이지
def feed_2(request):
    resume = Resume.objects.get(user=request.user)
    return render(request, "feed_2.html", {
        "card": resume.card,
    })


# 사료 구매(대두박)하는 페이지
def feed_3(request):
    resume = Resume.objects.get(user=request.user)
    return render(request, "feed_3.html", {
        "card": resume.card,
    })

