from django.db.models import Exists, OuterRef, Subquery
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.constants import LikeValue
from survey.models import Answer, Question, Like


class QuestionListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        qs = Question.objects.all()

        if self.request.user.pk:
            qs = qs.annotate(
                user_likes=Exists(
                    Like.objects.filter(
                        question=OuterRef("pk"),
                        author=self.request.user,
                        value=LikeValue.Liked,
                    )
                ),
                user_dislikes=Exists(
                    Like.objects.filter(
                        question=OuterRef("pk"),
                        author=self.request.user,
                        value=LikeValue.Disliked,
                    )
                ),
                user_value=Subquery(
                    Answer.objects.filter(
                        question=OuterRef("pk"), author=self.request.user
                    ).values("value")
                ),
            )

        return qs.order_by("-ranking")


class QuestionCreateView(CreateView):
    model = Question
    fields = ["title", "description"]
    redirect_url = ""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "survey/question_form.html"
