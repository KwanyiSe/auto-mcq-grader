from django.db import models

from django.db import models

class AnswerKey(models.Model):
    title = models.CharField(max_length=200)
    answers = models.JSONField()        # {"1":"A","2":"B",...}

    def __str__(self):
        return self.title

class Submission(models.Model):
    answer_key = models.ForeignKey(AnswerKey, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    uploaded_image = models.ImageField(upload_to='submissions/')
    score = models.IntegerField(null=True, blank=True)
    results = models.JSONField(null=True, blank=True)   # per-question details
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.answer_key.title}"