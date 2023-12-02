from django.urls import path

from survey.views import (
    QuestionListView,
    QuestionCreateView,
    QuestionUpdateView,
)

urlpatterns = [
    path("", QuestionListView.as_view(), name="question-list"),
    path("question/add/", QuestionCreateView.as_view(), name="question-create"),
    path("question/edit/<int:pk>", QuestionUpdateView.as_view(), name="question-edit"),
]
