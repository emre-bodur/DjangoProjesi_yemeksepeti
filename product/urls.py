from django.urls import path

from home import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    ]