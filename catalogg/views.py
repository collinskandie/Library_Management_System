from django.shortcuts import render
from django.views import generic

from catalogg.models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html',
                  context={
                      'num_books': num_books,
                      'num_instances': num_instances,
                      'num_instances_available': num_instances_available,
                      'num_authors': num_authors, }
                  )


# model = Book is really just shorthand for saying:
#                                                   queryset = Book.objects.all().

# class BookListView(generic.ListView):
#     model = Book
#     context_object_name = 'my_book_list'   # your own name for the list as a template variable
#     template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
#     queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

# class AcmeBookList(ListView):
#     context_object_name = 'book_list'
#     queryset = Book.objects.filter(publisher__name='ACME Publishing')
#     template_name = 'books/acme_list.html'

# class BookListView(generic.ListView):
#     model = Book
#
#     def get_queryset(self): # This is more flexible than "queryset" above :)
#         return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


# (From Below)
# All you need to do now is create a template called /locallibrary/catalog/templates/catalog/book_detail.html,
# and the view will pass it the database information for the specific Book record extracted by the URL mapper. Within
# the template you can access the list of books with the template variable named object OR book (i.e. generically
# "the_model_name").

# If you need to, you can change the template used and the name of the context object used to reference the book in the template. You can also override methods to, for example, add additional information to the context.

class BookDetailView(generic.DetailView):
    model = Book
