from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('articles/', views.ArticleList.as_view(), name='articles-list'),
    path('articles/category/<slug>/', views.ArticleCategoryList.as_view(), name='articles-category-list'),
    path('articles/<year>/<month>/<day>/<slug>/', views.ArticleDetail.as_view(), name='news-detail'),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("article/create", views.CreateArticle.as_view(), name="create-article"),  # fix after
]
