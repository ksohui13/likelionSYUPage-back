from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.question_create),
    path('', views.question_list, name='question_list'),
    path('<int:pk>', views.question_detail, name='question_detail'),
    path('update/<int:pk>', views.question_update, name='question_update'),
    path('delete/<int:pk>', views.question_delete, name='question_delete')
]