from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Fiszki
import random

# Create your views here.

def fiszki(request):
    message = ""

    if 'prev_word_id' in request.session:
        try:
            prev_word = Fiszki.objects.get(id=request.session['prev_word_id'], user=request.user)
        except Fiszki.DoesNotExist:
            prev_word = None
    else:
        prev_word = None

    if 'guessed_word' in request.POST and prev_word:
        guessed_word = request.POST.get('guessed_word')
        if guessed_word and guessed_word.strip() and guessed_word.lower() == prev_word.english_word.lower():
            prev_word.correct_guesses += 1
            prev_word.last_correct_guess = timezone.now()
            prev_word.save()
            message = "Correct! Well done!"
        elif guessed_word and guessed_word.strip():
            message = f"Incorrect! The correct word was: {prev_word.english_word}"
        del request.session['prev_word_id']

    words = Fiszki.objects.filter(user=request.user)
    if not words.exists():
        return render(request, 'fiszki/fiszki.html', {'error': 'No words available.'})

    current_word = random.choice(words)
    request.session['prev_word_id'] = current_word.id

    return render(request, 'fiszki/fiszki.html', {'word': current_word, 'message': message})

def new_fiszki(request):
    if request.method == 'POST':
        polish = request.POST.get('polish')
        english = request.POST.get('english')
        userid = 1
        if not Fiszki.objects.filter(polish_word=polish).exists():
            Fiszki.objects.create(polish_word=polish, english_word=english, user_id=userid)
        return redirect('create_new')
    return render(request, 'fiszki/new_fiszki.html')

def words(request):
    word_list = Fiszki.objects.all()
    return render(request, 'fiszki/word_list.html', {'word_list': word_list})

def revision(request):
    message = ""

    if 'prev_word_id' in request.session:
        try:
            prev_word = Fiszki.objects.get(id=request.session['prev_word_id'], user=request.user)
        except Fiszki.DoesNotExist:
            prev_word = None
    else:
        prev_word = None

    if request.method == 'POST' and prev_word:
        guessed_word = request.POST.get('guessed_word')
        if guessed_word and guessed_word.strip():
            if guessed_word.lower() == prev_word.english_word.lower():
                prev_word.correct_guesses += 1
                prev_word.last_correct_guess = timezone.now()
                prev_word.save()
                message = "Correct! Well done!"
            else:
                message = f"Incorrect! Try again! The first letter is: '{prev_word.english_word[0]}' and the word has {len(prev_word.english_word)} letters."
            del request.session['prev_word_id']

    words = Fiszki.objects.filter(user=request.user).order_by('last_correct_guess')
    if not words.exists():
        return render(request, 'fiszki/revision.html', {'error': 'No words available.'})

    current_word = words.first()
    request.session['prev_word_id'] = current_word.id

    return render(request, 'fiszki/revision.html', {'word': current_word, 'message': message})
