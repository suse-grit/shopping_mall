from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.CartsView.as_view())
]
