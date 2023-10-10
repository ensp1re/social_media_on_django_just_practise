from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    user = request.user
    hello = "Hello World!"

    context = {
        "user" : user,
        "hello" : hello
    }


    return render(request, 'main/home.html', context)