from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    
    path('tours/', views.tour_list, name='tours'),
    path('tours/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    
    path('guides/', views.guide_list, name='guide_list'),
    path('guides/<int:guide_id>/', views.guide_detail, name='guide_detail'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('create-tour/', views.create_tour, name='create_tour'),
    path('news/<int:post_id>/', views.post_detail, name='post_detail'),
    path('ticket/<int:reservation_id>/', views.view_ticket, name='view_ticket'),
    path('upgrade-request/', views.upgrade_to_leader, name='upgrade_to_leader'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)