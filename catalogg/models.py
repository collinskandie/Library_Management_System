# # Create your models here
#
# from django.db import models
# import uuid
# from django.urls import reverse
#
#
# class Genre(models.Model):
#     name = models.CharField(max_length=200, help_text="Enter a book genre")
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_of_death = models.DateField('Died', null=True, blank=True)
#
#     class Meta:
#         ordering = ['last_name', 'first_name']
#
#     def get_absolute_url(self):
#         return reverse('author-detail', args=[str(self.id)])
#
#     def __str__(self):
#         return f'{self.last_name},{self.first_name}'
#
#
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     # Foreign Key used because book can only have one author, but authors can have multiple books
#     author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
#     # ManyToManyField used because genre can contain many books. Books can cover many genres.
#     genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
#     summary = models.TextField(max_length=1000, help_text="Enter a brief description of the Book")
#     imprint = models.CharField(max_length=200)
#     # isbn specifies its label as "ISBN" using the first unnamed parameter because
#     # the default label would otherwise be "Isbn"
#     ISBN = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international'
#                                                              '.org/content/what-isbn">ISBN number</a>')
#
#     def __str__(self):
#         return self.title
#
#     # get_absolute_url() returns a URL that can be used to access a detail record for this model
#     # for this to work we will have to define a URL mapping that has the name book-detail,
#     # and define an associated view and template
#
#     # def get_absolute_url(self):
#     #     return reverse("book_detail", args=[str(self.id)])
#
#     def display_genre(self):
#         """Create a string for the Genre. This is required to display genre in Admin."""
#         return ', '.join(genre.name for genre in self.genre.all()[:3])
#
#     display_genre.short_description = 'Genre'
#
#
# class BookInstance(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text='Unique ID for this particular book '
#                                                                             'across whole library')
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name="books")
#     imprint = models.CharField(max_length=200)
#     date_due_back = models.DateField(null=True, blank=True)
#
#     LOAN_STATUS = (
#         ('o', 'On loan'),
#         ('a', 'Available'),
#     )
#
#     # tuple containing tuples of key-value pairs then pass it to the choices argument
#
#     status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text="Book Availability")
#
#     def __str__(self):
#         return f'{self.id}({self.book.title})'
#
#         # String for representing the Model Object
#
#         # The model __str__() represents the BookInstance object
#         # using a combination of its unique id and the associated Book's title.
#
#         # f-strings
#         # f'{self.id} ({self.book.title})'
#
#     class Meta:
#         ordering = ["date_due_back"]
#
#     # You can declare model - level metadata for your Model by declaring class Meta, as shown.
#     # One of the most useful
#     # features of this metadata is to control the default ordering of records returned when you query the model type.
#
#     # You do this by specifying the match order in a list of field names to the ordering attribute, as shown above.
#
#     # The ordering will depend on the type of field (character fields are sorted alphabetically, while date fields
#     # are sorted in chronological order)
#
#     # As shown above, you can prefix the field name with a minus symbol (-) to reverse the sorting order
from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    date_due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.date_due_back and date.today() > self.date_due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['date_due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
