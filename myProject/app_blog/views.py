from django.views.generic import DateDetailView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Article, Category
from .forms import UserRegisterForm, ArticleImageForm, AddArticleForm
from django.views.generic.edit import CreateView


class HomePageView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(main_page=True)[:5]

        return context


class ArticleDetail(DateDetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'item'
    date_field = 'pub_date'
    query_pk_and_slug = True
    month_format = "%m"
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['image'] = context['item'].images.all()
        except:
            pass

        return context


class ArticleList(ListView):
    model = Article
    queryset = Article.objects.all()
    template_name = 'articles_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["category"] = Category.objects.get(slug=self.kwargs.get("slug"))
        except:
            context["category"] = None

        return context


class ArticleCategoryList(ArticleList):
    def get_queryset(self):
        return super().get_queryset().filter(category__slug__in=[self.kwargs.get("slug")]).distinct()


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'user_register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class CreateArticle(SuccessMessageMixin, TemplateView):
    template_name = 'article_create.html'
    article_form_class = AddArticleForm
    image_form_class = ArticleImageForm
    success_message = "Your article was created successfully"

    def post(self, request):
        post_data = request.POST or None
        post_files = request.FILES or None
        article_form = self.article_form_class(post_data, prefix="article")
        image_form = self.image_form_class(post_data, post_files, prefix="image")

        context = self.get_context_data(article_form=article_form, image_form=image_form)

        if article_form.is_valid() and image_form.is_valid():
            article = article_form.save(commit=False)
            article_image = image_form.save(commit=False)
            article.author = request.user
            article.slug = slugify(article.title)
            article.save()
            article_image.article = article
            article_image.save()
            return redirect("home")

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request)
