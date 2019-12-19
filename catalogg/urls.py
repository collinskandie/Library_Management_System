from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    # For Django class-based views we access an appropriate view function by calling the class method as_view()
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail')]
