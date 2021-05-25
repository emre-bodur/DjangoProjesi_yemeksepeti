import json
import urllib.request
from unicodedata import category
from urllib.error import HTTPError

from ckeditor_uploader.forms import SearchForm
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Content, CImages, Menu
from home.forms import SingUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile, FAQ
from order.models import ShopCart
from product.models import Product, Category, Images, Comment, Restaurant


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    sliderdata = Product.objects.all()[:4]
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:6]
    randomproducts = Product.objects.all().order_by('?')[:6]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    news = Content.objects.filter(type='haber', status=True).order_by('-id')[:6]
    announcements = Content.objects.filter(type='duyuru', status=True).order_by('-id')[:6]
    restaurant = Restaurant.objects.all()
    restaurant1 = Restaurant.objects.all()
    context = {'setting': setting,
               'restaurant': restaurant,
               'restaurant1': restaurant1,
               'category': category,
               'page': 'home',
               'menu': menu,
               'sliderdata': sliderdata,
               'news': news,
               'announcements': announcements,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts': randomproducts}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    context = {'restaurant1': restaurant1,
               'setting': setting,
               'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    restaurant1 = Restaurant.objects.all()
    category = Category.objects.all()
    context = {'setting': setting,
               'page': 'referanslar',
               'restaurant1': restaurant1,
               'category': category}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkürler.")
            return HttpResponseRedirect('/iletisim')

    restaurant1 = Restaurant.objects.all()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactFormu()
    context = {'setting': setting,
               'form': form,
               'category': category,
               'restaurant1': restaurant1
               }
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    restaurant1 = Restaurant.objects.all()
    comments = Comment.objects.filter(product_id=id, status='True')
    products = Product.objects.filter(category_id=id)
    context = {
        'products': products,
        'category': category,
        'catdata': catdata,
        'comments': comments,
        'restaurant1': restaurant1,
    }
    return render(request, 'category_products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    current_user = request.user
    restaurant1 = Restaurant.objects.all()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity
    try:
        product = Product.objects.get(pk=id)
        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id, status='True')
        context = {
            'total': total,
            'schopcart': schopcart,
            'product': product,
            'category': category,
            'Images': Images,
            'comments': comments,
            'restaurant1': restaurant1,

        }
        return render(request, 'product_detail.html', context)
    except:
        messages.warning(request, "Hata! ilgili içerik bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)


def product_search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # get form input data
            products = Product.objects.filter(title__icontains=query)

            context = {'products': products, 'category': category}
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)  # şehirlere göre yapabilirsin video 21.
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş yapılamadı! Kullanıcı adı veya şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    context = {
        'category': category,
        'restaurant1': restaurant1,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']  # şifre hatası verirse password1 yapcan emmi
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Hoş geldiniz...Sitemize Başarılı bir şekilde üye oldunuz.')
            return HttpResponseRedirect('/')

    form = SingUpForm()
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    context = {
        'category': category,
        'restaurant1': restaurant1,
        'form': form,
    }
    return render(request, 'signup.html', context)


def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    restaurant1 = Restaurant.objects.all()
    context = {
        'category': category,
        'restaurant1': restaurant1,
        'menu': menu,
    }

    return render(request, '404.html', context)


def contentdetail(request, id, slug):
    try:
        category = Category.objects.all()
        menu = Menu.objects.all()
        # comments= Comment.objects.filter(product.id=id,status=True)
        content = Content.objects.get(pk=id)
        restaurant1 = Restaurant.objects.all()
        images = CImages.objects.filter(content_id=id)
        context = {
            # 'comments': comments,
            'content': content,
            'category': category,
            'restaurant1': restaurant1,
            'menu': menu,
            'images': images,
        }

        return render(request, 'content_detail.html', context)
    except:
        messages.warning(request, "Hata! ilgili içerik bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)


def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "Hata! ilgili içerik bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)


def faq(request):
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    menu = Menu.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'faq': faq,
        'category': category,
        'menu': menu,
        'restaurant1': restaurant1,
    }

    return render(request, 'faq.html', context)


def restaurant(request, id):
    category = Category.objects.all()
    restaurants = Restaurant.objects.get(id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    products = Product.objects.filter(restaurant_id=id)
    restaurant = Restaurant.objects.filter(id=id)
    restaurant1 = Restaurant.objects.all()
    context = {
        'products': products,
        'category': category,
        'comments': comments,
        'restaurant': restaurant, 'restaurants': restaurants, 'restaurant1': restaurant1,

    }
    return render(request, 'restaurant.html', context)
