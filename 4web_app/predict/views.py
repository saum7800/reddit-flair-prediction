from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import praw
import ktrain
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'distilbert_predictor_final')
predictor = ktrain.load_predictor(my_file)
# Create your views here.


def get_submission_from_url(submission_url):
    reddit = praw.Reddit(client_id='2uReEcmijpNWnw',
                         client_secret='V0PCW7O1S6r3prN6ieRr4LVPGKo', user_agent='test reddit app')
    submission = None
    if submission_url.startswith('www'):
        submission_url = "https://" + submission_url
    elif submission_url.startswith('reddit'):
        submission_url = "https://www." + submission_url

    if submission_url.startswith('https://'):
        submission = reddit.submission(url=submission_url)
    return submission


def get_data_from_post(submission_url):

    submission = get_submission_from_url(submission_url)
    if submission is not None:
        full_text = submission.title + submission.selftext
        prediction = predictor.predict(full_text)
        card_color = None
        if(prediction == submission.link_flair_text):
            card_color = "success"
        else:
            card_color = "danger"
        sub_details = {'title': submission.title, 'selftext': submission.selftext, 'score': submission.score, 'num_comments': submission.num_comments,
                       'flair': submission.link_flair_text, 'prediction': prediction, 'card_color': card_color, 'render': True}
        return sub_details
    else:
        return None


def home(request):

    if request.method == 'POST':
        submission_url = request.POST['URL']
        context = get_data_from_post(submission_url)
        if context is None:
            messages.error(request, f'Incorrect URL')
            context = {'render': False}
        return render(request, 'predict/home.html', context)
    else:
        return render(request, 'predict/home.html', {'render': False})


def about(request):
    return render(request, 'predict/about.html', {'title': 'About'})


def get_final_dict(url_file):
    urls = url_file.split('\n')
    if(not urls[len(urls)-1]):
        urls.pop(len(urls)-1)

    submissions = [get_submission_from_url(
        submission_url) for submission_url in urls]
    
    if None in submissions:
        return None
    else:
        full_texts = [submission.title +
                    submission.selftext for submission in submissions]
        prediction = predictor.predict(full_texts)
        final_dict = {urls[i]: prediction[i] for i in range(len(urls))}
        return final_dict


def automated_testing(request):

    if request.method == 'POST':
        url_file = (request.FILES['upload_file']).read()
        url_file = url_file.decode("utf-8")
        data = get_final_dict(url_file)
        if data is None:
            messages.error(request, f'Incorrect URL')
            return redirect('predict-automated_testing')
        else:
            return JsonResponse(data)
        # return render(request, 'predict/automated_testing.html', context)
    else:
        return render(request, 'predict/automated_testing.html', {'render': False})
