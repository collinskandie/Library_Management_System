# Create your models here

from django.db import models
import uuid
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the Book")
    imprint = models.CharField(max_length=200)
    # isbn specifies its label as "ISBN" using the first unnamed parameter because
    # the default label would otherwise be "Isbn"
    ISBN = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international'
                                                             '.org/content/what-isbn">ISBN number</a>')

    def __str__(self):
        return self.title

    # get_absolute_url() returns a URL that can be used to access a detail record for this model
    # for this to work we will have to define a URL mapping that has the name book-detail,
    # and define an associated view and template

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text='Unique ID for this particular book '
                                                                            'across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    date_due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
    )

    # tuple containing tuples of key-value pairs then pass it to the choices argument

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text="Book Availability")

    def __str__(self):
        return f'{self.id}({self.book.title})'

        # String for representing the Model Object

        # The model __str__() represents the BookInstance object
        # using a combination of its unique id and the associated Book's title.

        # f-strings
        # f'{self.id} ({self.book.title})'

    class Meta:
        ordering = ["date_due_back"]

    # You can declare model - level metadata for your Model by declaring class Meta, as shown.
    # One of the most useful
    # features of this metadata is to control the default ordering of records returned when you query the model type.

    # You do this by specifying the match order in a list of field names to the ordering attribute, as shown above.

    # The ordering will depend on the type of field (character fields are sorted alphabetically, while date fields
    # are sorted in chronological order)

    # As shown above, you can prefix the field name with a minus symbol (-) to reverse the sorting order
