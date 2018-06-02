from django.shortcuts import render, redirect
from accounts.models import Resume
from .forms import OrderForm
from .loop import run_transaction, check_last
from .socket_server import run_server


# 사료 구매 / 고기 구매
def main(request):
    return render(request, "main.html")


# 사료 종류 보는 페이지
def feed(request):
    return render(request, "feed.html")


# 고기 구매하는 페이지
def meat(request):
    return render(request, "meat.html")


# 결과 나오는 페이지
def result(request):
    ret = check_last(1527952680, 152700952683)
    b_ret = []
    dic = {}
    for x in ['corn', 'rice', 'soybean']:
        dic[x] = 0
    for x in ret:
        # print(x['card'])
        if x['card'] == '1238-1241-2387-7812':
            dic[x['element']] += int(x['amount'])
            b_ret.append(x)
    # print(ret)
    return render(request, "result.html", {
        "corn": int(dic['corn']),
        "rice": int(dic['rice']),
        "soybean": int(dic['soybean']),
        "ret": b_ret,
    })


# 사료 구매(옥수수)하는 페이지
def feed_1(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            run_transaction(0, form.cleaned_data['card'], form.cleaned_data['element'], int(form.cleaned_data['amount']) * 300)
            msg = run_server(4000, "2:" + str(30 * form.cleaned_data['amount']))
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_1.html", {
            "card": resume.card,
            "form": form,
            "msg": msg,
        })
    else:
        form = OrderForm(initial={'card': request.user.resume_set.card, 'element': 'corn', 'amount': 1})
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_1.html", {
            "card": resume.card,
            "form": form,
        })
    else:
        return render(request, "feed_1.html", {
            "form": form,
        })


# 사료 구매(쌀겨)하는 페이지
def feed_2(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            run_transaction(0, form.cleaned_data['card'], form.cleaned_data['element'], int(form.cleaned_data['amount']) * 200)
            msg = run_server(4000, "2:" + str(25 * form.cleaned_data['amount']))
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_2.html", {
            "card": resume.card,
            "form": form,
            "msg": msg,
        })
    else:
        form = OrderForm(initial={'card': request.user.resume_set.card, 'element': 'rice', 'amount': 1})
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_2.html", {
            "card": resume.card,
            "form": form,
        })
    else:
        return render(request, "feed_2.html", {
            "form": form,
        })


# 사료 구매(대두박)하는 페이지
def feed_3(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            run_transaction(0, form.cleaned_data['card'], form.cleaned_data['element'], int(form.cleaned_data['amount']) * 150)
            msg = run_server(4000, "2:" + str(11 * form.cleaned_data['amount']))
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_3.html", {
            "card": resume.card,
            "form": form,
            "msg": msg,
        })
    else:
        form = OrderForm(initial={'card': request.user.resume_set.card, 'element': 'soybean', 'amount': 1})
    if Resume.objects.filter(user=request.user).exists():
        resume = Resume.objects.get(user=request.user)
        return render(request, "feed_3.html", {
            "card": resume.card,
            "form": form,
        })
    else:
        return render(request, "feed_3.html", {
            "form": form,
        })


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
