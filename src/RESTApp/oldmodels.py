from django.db import models

LANGUAGE_CHOICES = [
    ("python", "Python"),
    ("Csharp", "C#")
]


# Create your models here.
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='Python', max_length=100)

    class Meta:
        ordering = ('created',)
