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
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_1.html", {
            "card": resume.card,
        })
    else:
        return render(request, "feed_1.html")


# 사료 구매(쌀겨)하는 페이지
def feed_2(request):
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_2.html", {
            "card": resume.card,
        })
    else:
        return render(request, "feed_2.html")


# 사료 구매(대두박)하는 페이지
def feed_3(request):
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_3.html", {
            "card": resume.card,
        })
    else:
        return render(request, "feed_3.html")


# 고기 구매(소고기)하는 페이지
def meat_1(request):
    # resume = Resume.objects.get(user=request.user)
    return render(request, "meat_1.html", {
        # "location": resume.location,
    })


# 고기 구매(돼지고기)하는 페이지
def meat_2(request):
    # resume = Resume.objects.get(user=request.user)
    return render(request, "meat_2.html", {
        # "location": resume.location,
    })


# 고기 구매(닭고기)하는 페이지
def meat_3(request):
    # resume = Resume.objects.get(user=request.user)
    return render(request, "meat_3.html", {
        # "location": resume.location,
    })

