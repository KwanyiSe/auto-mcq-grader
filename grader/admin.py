from django.contrib import admin
from .models import AnswerKey, Submission
# registering our models so we can see them in admin boring admin because it does not really have a use 
@admin.register(AnswerKey)
class AnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answers')   # removed questions_count
    search_fields = ('title',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'answer_key', 'score', 'graded_at')
    list_filter = ('answer_key', 'graded_at')