from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# <HINT> Register QuestionInline and ChoiceInline classes here


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('course', 'short_question_text', 'grade_point')
    search_fields = ('question_text',)
    list_select_related = ('course',)

    def short_question_text(self, obj):
        return (obj.question_text[:75] + '...') if len(obj.question_text) > 75 else obj.question_text
    short_question_text.short_description = 'Question'

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'content', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('content',)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'enrollment', 'created_at', 'submission_score')
    search_fields = ('enrollment__user__username', 'enrollment__course__name')
    filter_horizontal = ('choices',)

    def submission_score(self, obj):
        return obj.total_score()
    submission_score.short_description = 'Score'

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


# <HINT> Register Question and Choice models here

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
