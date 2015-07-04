---
layout: post
title: Просто о Django Content Types Framework
tags: "python, django"
category: ru
---

Появилась задача реализовать функцию комментариев для пяти моделей через одну.

Небольшой пример, как это могло выглядеть без Content Types Framework:

{% highlight python %}
class Comment(models.Model):
    user = models.ForeignKey('User', related_name='comment')
    title = models.CharField(max_length=255)
    body = models.TextField()

    article = models.ForeignKey('Article', related_name='comment')
    todo = models.ForeignKey('ToDo', related_name='comment')
    blog_post = models.ForeignKey('BlogPost', related_name='comment')
    image = models.ForeignKey('Image', related_name='comment')
    album = models.ForeignKey('Album', related_name='comment')
{% endhighlight %}

Пример с Content Types:

{% highlight python %}
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    user = models.ForeignKey('User', related_name='comment')
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

{% endhighlight %}

Куда более компактный код, не так ли?

И так, что же такое Content Types Framework и как он работает?

Content Types Framework сохраняет информацию о моделях в таблицу contenttypes, а именно: название приложения, название модели и тип. Таким образом мы можем создать GenericForeignKey на любую модель используя всего одно поле.

Получить объект Content Type можно двумя способами:

по классу нашей модели

{% highlight python %}
ContentType.objects.get_for_model(Article)
{% endhighlight %}

или по названию модели

{% highlight python %}
from django.contrib.contenttypes.models import ContentType
article_type = ContentType.objects.get(app_label='core', model='article')

{% endhighlight %}

теперь можно получить модель через Content Type Object:

{% highlight python %}
model = user_type.model_class()
{% endhighlight %}

Это бывает очень удобно, например, если мы хотим получить список статей, картинок, альбомов через шаблон из URL используя только одно представление:

{% highlight python %}
class MyTypes(View):
    def get(self, request, *args, **kwargs):
        content_type_name = kwargs.get('name')

        # Получаем content type по названию модели из url
        content_type = get_object_or_404(ContentType, name=content_type_name)

        # Получаем модель
        model = content_type.get_for_model()
        context = {
            'objects': model.objects.all()
        }
{% endhighlight %}

Так можно получить список комментариев определенной статьи

{% highlight python %}
first_article = Article.objects.get(pk=1)
content_type = ContentType.objects.get_for_model(first_article)
object_list = Comment.objects.filter(
    content_type__pk=content_type.pk,
    object_id=first_article.pk
)
{% endhighlight %}
