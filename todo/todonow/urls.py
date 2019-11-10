from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin_homepage/', views.admin_view, name='admin_homepage'),
    path('approve_complete/<int:pk>/', views.approve_completed, name='approve'),
    path('create/', views.todo_create_view, name="create"),
    path('delete/<int:pk>/', views.delete_todo, name='delete'),
    path('details/<int:pk>/', views.todo_detail, name='details'),
    path('profile/', views.profile_page, name='profile'),
    path('update_complete/<int:pk>/', views.update_completed_status, name='updatecomplete'),
    path('update/<int:pk>/', views.update_todo_view.as_view(), name='update'),
    path('usertodos/<int:pk>/', views.user_todos, name='user_todos'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
