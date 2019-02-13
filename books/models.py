from django.db import models
from isbn_field import ISBNField
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
	book_name = models.CharField(max_length=120)
	image = models.ImageField(upload_to='bookpic', null=True, blank=True)
	conditions = (
	('New', 'New'),
    ('Used', 'Used'),
	)
	condition = models.CharField(
		max_length = 5,
		choices = conditions,
		default = 'New',
	)
	isbn = ISBNField(clean_isbn=False)
	author = models.CharField(max_length=120)

	def __str__(self):
		return "%s by %s" % (self.book_name, self.author)

class MyBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
