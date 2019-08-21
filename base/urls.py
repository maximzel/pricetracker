from django.urls import path
from pricetracker.settings import SECRET_URL
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('rubric/<int:rubric_id>/', views.rubric, name='rubric'),
    path('market/<int:market_id>/', views.market, name='market'),
    path('search/', views.search, name='search'),
    path(SECRET_URL, views.update, name='update'),
]
