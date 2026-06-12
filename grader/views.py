from django.shortcuts import render, redirect, get_object_or_404
from .models import AnswerKey, Submission
from .grading import grade_submission
import os
import shutil
from django.conf import settings
from django.templatetags.static import static


def home(request):
    answer_keys = AnswerKey.objects.all()
    return render(request, 'grader/home.html', {'answer_keys': answer_keys})

def create_answer_key(request):
    if request.method == 'POST':
        title = request.POST['title']
        answers = {}
        for i in range(1, 11):
            ans = request.POST.get(f'q{i}')
            if ans:
                answers[str(i)] = ans
        AnswerKey.objects.create(title=title, answers=answers)
        return redirect('home')
    return render(request, 'grader/create_key.html')

def upload_and_grade(request):
    if request.method == 'POST':
        key_id = request.POST['answer_key']
        student_name = request.POST['student_name']
        image = request.FILES['image']
        key = get_object_or_404(AnswerKey, id=key_id)

        submission = Submission.objects.create(
            answer_key=key,
            student_name=student_name,
            uploaded_image=image
        )
        score, results, _ = grade_submission(submission.uploaded_image.path, key.answers)
        submission.score = score
        submission.results = results
        submission.save()

        return render(request, 'grader/result.html', {
            'submission': submission,
            'results': results,
            'total': len(key.answers),
        })
    return redirect('home')


def sample_grade(request):
    # --- Copy sample image to media for grading ---
    sample_src = os.path.join(settings.BASE_DIR, 'grader', 'static', 'samples', 'test_sheet.png')
    media_dir = os.path.join(settings.MEDIA_ROOT, 'samples')
    os.makedirs(media_dir, exist_ok=True)
    media_path = os.path.join(media_dir, 'test_sheet.png')
    shutil.copy(sample_src, media_path)

    key = AnswerKey.objects.get(id=1)

    submission = Submission.objects.create(
        answer_key=key,
        student_name="Sample Student",
        uploaded_image='samples/test_sheet.png'
    )

    score, results, _ = grade_submission(media_path, key.answers)
    submission.score = score
    submission.results = results
    submission.save()

    # Get the static URL of the sample image for display
    sample_image_url = static('samples/test_sheet.png')

    return render(request, 'grader/result.html', {
        'submission': submission,
        'results': results,
        'total': len(key.answers),
        'sample_image_url': sample_image_url,   # pass the image URL
    })