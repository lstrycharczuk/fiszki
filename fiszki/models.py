from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Fiszki(models.Model):
    polish_word = models.CharField(max_length=100)
    english_word = models.CharField(max_length=100)
    correct_guesses = models.IntegerField(default=0)
    last_correct_guess = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.polish_word + ' - ' + self.english_word + ', ' + self.last_correct_guess.strftime('%Y-%m-%d %H:%M:%S')
