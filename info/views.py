from django.shortcuts import render


def index(request):
    return render(request, 'info/index.html')


def contact(request):
    return render(request, 'info/contact.html')


def faq(request):
    return render(request, 'info/faq.html')


def about(request):
    return render(request, 'info/about.html')
