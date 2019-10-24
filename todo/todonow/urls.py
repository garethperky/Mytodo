from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create/', views.todo_create_view, name="create"),
    path('overall/', views.todo_group_view, name="overall")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
