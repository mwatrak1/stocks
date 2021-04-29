from django.urls import path
from . import views
from . import graphs


urlpatterns = [
    path('', views.index, name='index'),
    path('user/dashboard/', views.dashboard, name='dashboard'),
    path('stocks/', views.stocks, name='stocks'),
    path('user/login/', views.login, name='login'),
    path('user/register/', views.register, name='register'),
    path('user/logout/', views.logout, name='logout'),
    path('addNotification/', views.add_notification, name='add_notification'),
    path('deleteNotification/', views.delete_notification, name="delete_notification"),
    path('getStocksGraph/<abbreviation>/', graphs.render_graph, name='render_graph'),
    path('telegram/update/', views.telegram_update, name='telegram_update')
]