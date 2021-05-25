from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import ContentForm, Content
from home.models import UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product, Restaurant

from django.utils.crypto import get_random_string


def index(request):
    return HttpResponse("Order App")


@login_required(login_url='/login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün Başarı ile sepete eklenmiştir...0")
        return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            current_user = request.user
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün Başarı ile sepete eklenmiştir Teşekkürlrer")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürünü sepete eklemede  hata oluştu!, Lütfen tekrar deneyiniz")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    restaurant1 = Restaurant.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = {
        'schopcart': schopcart,
        'restaurant1': restaurant1,
        'category': category,
        'total': total,
    }

    return render(request, "Shopcart_products.html", context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün Sepetinizden Silinmiştir")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')
def deletefromcart1(request, id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    link = '/product/' + str(product.id) + str(product.slug)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün Sepetinizden Silinmiştir")
    return HttpResponseRedirect(link)


@login_required(login_url='/login')
def orderproduct(request):
    restaurant1 = Restaurant.objects.all()
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # stoktan düşme
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Siparişiniz tamamlandı")
            return render(request, 'Order_Complated.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    restaurant1 = Restaurant.objects.all()
    context = {'restaurant1': restaurant1,
               'schopcart': schopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }

    return render(request, 'Order_Form.html', context)


def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "Hata! ilgili içerik bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)


def contentdetail(request, id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    restaurant1 = Restaurant.objects.all()
    content = Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id=id)
    context = {
        'content': content,
        'category': category,
        'restaurant1': restaurant1,
        'menu': menu,
        'images': images,
    }

    return render(request, 'content_detail.html', context)


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


@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    restaurant1 = Restaurant.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'restaurant1': restaurant1,
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_contents.html', context)


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
    Content.objects.filter(id=id, user_id=current_user.id).delete()()
    messages.success(request, 'İçerik Silindi...')
    return HttpResponseRedirect('/user/contents')


