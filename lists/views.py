from django.shortcuts import render, redirect
from lists.models import Item


# Создайте ваши представления здесь.
def home_page(request):
    """домашняя страница"""
    return render(request, 'home.html')


def view_list(request):
    """представление списка"""
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(requst):
    """новый список"""
    Item.objects.create(text=requst.POST['item_text'])
    return redirect('/lists/one-single-list-in-the-world/')
