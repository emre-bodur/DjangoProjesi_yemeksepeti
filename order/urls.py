from django.urls import path

from order import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
]
