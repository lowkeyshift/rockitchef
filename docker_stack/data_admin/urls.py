from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', views.home, name='home'),
    path('edit/<int:pk>', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:pk>', views.delete_recipe, name='delete_recipe'),
    path('dashboard/', views.dashboard, name='dashboard'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
