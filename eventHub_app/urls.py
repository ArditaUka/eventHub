from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('display_login', views.display_login),
    path('display_register', views.display_register),
    path('dashboard', views.dashboard),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('new_event', views.new_event),
    path('create_event', views.create_event),
    path('display_category/<str:category>', views.display_category),
    path('display/<int:event_id>', views.display),
    path('add_to_cart/<int:event_id>', views.add_to_cart),
    path('buy/<int:event_id>', views.buy),
    path('cart', views.cart),
    path('oneCart/<int:event_id>', views.one_cart),
    path('buy_ticket/<int:event_id>', views.buyTicket),
]
