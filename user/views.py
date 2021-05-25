import concurrent.futures
from tkinter import Menu
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import message
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile
from content.models import Content, Menu, ContentForm, ContentImageForm, CImages
from order.models import Order, OrderProduct, ShopCart
from product.models import Category, Comment, Restaurant
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    restaurant1 = Restaurant.objects.all()

    context = {
        'category': category,
        'restaurant1': restaurant1,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            message.success(request, 'Hesabın Güncellendi')
            return redirect('/user')

    else:
        category = Category.objects.all()
        restaurant1 = Restaurant.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'restaurant1': restaurant1,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            currentuser = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            message.success(request, 'içerik başarı ile eklendi')
            return HttpResponseRedirect('/user/contents')

        else:
            message.success(request, 'Hata:' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')

    else:
        category = Category.objects.all()
        restaurant1 = Restaurant.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'menu': menu,
            'category': category,
            'form': form,
            'restaurant1': restaurant1,
        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesap bilgileri güncellendi!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        restaurant1 = Restaurant.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'restaurant1': restaurant1,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz Başarı ile Güncellenmiştir!')
            return redirect('change_password')
        else:
            messages.error(request, 'Şifre Degiştirme Başarısız Lütfen Tekrar Deneyin')

    else:
        category = Category.objects.all()
        restaurant1 = Restaurant.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {'form': form, 'category': category, 'restaurant1': restaurant1})


@login_required(login_url='/login')
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    restaurant1 = Restaurant.objects.all()
    profile = UserProfile.objects.get(user_id=current_user.id)
    orders = Order.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'orders': orders,
        'profile': profile,
        'restaurant1': restaurant1,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')
def orderdetail(request, id):
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'restaurant1': restaurant1,
        'profile': profile,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    comments = Comment.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'restaurant1': restaurant1,
        'comments': comments,
        'profile': profile,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()

    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def contentdelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçerik Silindi.')
    return HttpResponseRedirect('/user/contents')


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'içeriginiz Başarı ile Eklenmiştir.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'İçerik hatası:' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')


    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        restaurant1 = Restaurant.objects.all()
        form = ContentForm()
        context = {
            'menu': menu,
            'category': category,
            'form': form,
            'restaurant1': restaurant1,
        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentedit(request, id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, ' İçerigin Başarı ile Güncellendi.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'içerik Ekleme Hatası' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' + str(id))

    else:
        category = Category.objects.all()
        restaurant1 = Restaurant.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'form': form,
            'menu': menu,
            'restaurant1': restaurant1,
        }
    return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentdelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçerik Silindi...')
    return HttpResponseRedirect('/user/contents')


@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    restaurant1 = Restaurant.objects.all()
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'profile': profile,
        'restaurant1': restaurant1,
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_contents.html', context)


def contentaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Resim Başarı ile yüklendi')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form error:' + str(form.errors))
            return HttpResponseRedirect(lasturl)

    else:
        content = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = ContentImageForm()
        context = {
            'content': content,
            'images': images,
            'form': form,

        }
        return render(request, 'content_gallery.html', context)


def shopcart(request):
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = {
        'schopcart': schopcart,
        'profile': profile,
        'category': category,
        'restaurant1': restaurant1,
        'total': total,
    }

    return render(request, 'user_shopcart.html', context)
