from django.contrib import admin
from .models import Author, BookInstance, Book, Genre

# Register your models here


# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)





class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Author, AuthorAdmin)





class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]





class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','book','status','date_due_back')
    list_filter = ('status', 'date_due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'date_due_back')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)
