from django.shortcuts import render


# 사료 구매 / 고기 구매
def main(request):
    return render(request, "main.html")


# 사료 구매하는 페이지
def feed(request):
    return render(request, "feed.html")


# 고기 구매하는 페이지
def meat(request):
    return render(request, "meat.html")
