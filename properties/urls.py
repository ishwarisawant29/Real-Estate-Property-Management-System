from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('inquiry/<int:pk>/', views.inquiry, name='inquiry'),
    path('visit/<int:pk>/', views.visit, name='visit'),
    path('review/<int:pk>/', views.review, name='review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('visit-status/<int:pk>/<str:status>/', views.update_visit_status, name='update_visit_status'),
    path('inquiry-reply/<int:pk>/', views.reply_inquiry, name='reply_inquiry'),
    path('notifications/', views.notifications, name='notifications'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<int:pk>/', views.edit_property, name='edit_property'),
    path('delete-property/<int:pk>/', views.delete_property, name='delete_property'),
    path('property/<int:pk>/add-image/', views.add_property_image, name='add_property_image'),
]
