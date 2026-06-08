# Django Online Course Project

A Django-based online course management system with admin features, course details, exams, and submissions.

## Features

- Course catalog with enrollment
- Lessons and exam questions
- Authentication and authorization
- Admin site for managing content
- Bootstrap-styled templates

## Project Structure

```
django-onlinecourse/
└── onlinecourse/
    ├── models.py          # Question, Choice, Submission models
    ├── admin.py           # Admin configurations
    ├── views.py           # submit and show_exam_result functions
    ├── urls.py            # URL routing
    └── templates/
        └── onlinecourse/
            └── course_details_bootstrap.html
```

**ER Diagram**
For your reference, we have prepared the ER diagram design for the new assesement feature.
![Onlinecourse ER Diagram](https://github.com/ibm-developer-skills-network/final-cloud-app-with-database/blob/master/static/media/course_images/onlinecourse_app_er.png)
