import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid
from django.core.validators import MinValueValidator


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

class Question(models.Model):
    """
    Questions for an exam related to a Course.
    - Many-to-one relationship with Course (a Course can have many Questions).
    - Stores the question text and a grade point value for the question.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    grade_point = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0)],
        help_text="Puntos/valor de la pregunta en la evaluación"
    )

    def __str__(self):
        # Muestra una versión corta del texto y curso para identificarla
        text_preview = (self.question_text[:50] + '...') if len(self.question_text) > 50 else self.question_text
        return f"{self.course.name} - {text_preview} ({self.grade_point})"

class Choice(models.Model):
    """
    Opciones para una Question.
    - Many-to-One con Question.
    - Texto de la opción y booleano indicando si es correcta.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        short = (self.content[:50] + '...') if len(self.content) > 50 else self.content
        status = 'correcta' if self.is_correct else 'incorrecta'
        # Evitar excepciones si question o course faltan
        curso = self.question.course.name if getattr(self, 'question', None) and getattr(self.question, 'course', None) else ''
        return f"{curso} - {short} ({status})"

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Submission(models.Model):
    """
    A Submission represents an exam submission for a given Enrollment.
    - Many-to-One with Enrollment (one enrollment can have multiple submissions).
    - Many-to-Many with Choice to store selected choices for this submission.
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.enrollment.user.username if self.enrollment and self.enrollment.user else 'unknown'
        course = self.enrollment.course.name if self.enrollment and self.enrollment.course else 'unknown'
        return f"Submission {self.id} by {user} for {course} at {self.created_at}"

    def total_score(self):
        """
        Compute total score for this submission by summing grade_point for questions
        where the selected choices are correct. This is a simple example and assumes
        choice.is_correct represents correctness of that choice.
        """
        # Sum grade_point for distinct questions where at least one selected choice is correct.
        scored_questions = set()
        score = 0.0
        for choice in self.choices.select_related('question').all():
            if choice.is_correct and choice.question_id not in scored_questions:
                score += choice.question.grade_point
                scored_questions.add(choice.question_id)
        return score

    def clean(self):
        """
        Validate that all selected choices belong to the same course as the enrollment.
        Raises ValidationError if any choice does not belong to the course.
        """
        from django.core.exceptions import ValidationError
        if not self.enrollment:
            return
        course = self.enrollment.course
        invalid = []
        for choice in self.choices.all():
            if choice.question.course_id != course.id:
                invalid.append(choice.id)
        if invalid:
            raise ValidationError("One or more selected choices do not belong to the course of the enrollment.")

# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
#class Submission(models.Model):
#    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
#    choices = models.ManyToManyField(Choice)
