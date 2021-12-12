import uuid
from django.db import models
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(_("Name"), max_length= 200, help_text= 'Enter a book Genre (e.g. Science Fiction)')

    def _str_(self):
        """String for representing the Model object."""
        return self.name


    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", kwargs={"pk": self.pk})

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null=True)

    summary = models.TextField(max_length=10000, help_text ='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href =  "https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='select a genre for this book')

    def _str_(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book:"""
        return reverse('book-detail', args =[str(self.id)])

    import uuid
class BookInstance(models.Model):
        """Model representing a specific copy of (i.e. that can be borrowed from the library)."""
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
        book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
        imprint = models.CharField(max_length=200)
        due_back= models.DateField(null=True, blank=True)

        Loan_Status = (
            ('m', 'Maintenance'),
            ('o', 'On Loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

        status = models.CharField(
            max_length=1,
            choices= Loan_Status,
            blank = True,
            default = 'm',
            help_text = 'Book Availability',
        )
        class Meta:
            ordering = ['due_back']

        def _str_(self):
           """String for representing the Model object."""
           return f'{self.id} ({self.book.title})'

class Author(models.Model):
     """Model representing an author."""
     first_name= models.CharField(max_length=100)
     last_name= models.CharField(max_length=100)
     date_of_birth= models.DateField(null = True, blank = True)
     date_of_death= models.DateField('died', null = True, blank = True)

class Meta:
         ordering=['last_name', 'first_name']

         def get_absolute_url(self):
           """Return the url to access a particular author instance."""
           return reverse('author-detail', args= [str(self.id)])

         def _str_(self):
           """String for representing the Model object."""
           return f'{self.last_name}, {self.first_name}'