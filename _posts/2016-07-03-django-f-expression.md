---
layout: post
title: F выражение в Django ORM
tags: "python, django"
category: ru
---

Выражение F() в Django ORM позволит вам использовать поля текущей модели в ваших запросах.

Например, вы хотите увеличить значение поля на единицу, на ум приходит следующий код:

{% highlight python %}

article = Article.objects.get(pk=1)
article.count += 1
article.save()

{% endhighlight %}

Но данный код можно реализовать более элегантным способом:

{% highlight python %}

Article.objects.filter(pk=1).update(count=F('count') + 5)

{% endhighlight %}

Более практичный пример, сравнивать поля текущей модели.

{% highlight python %}

In [2]: Article.objects.create(count=1, number_of_likes=10)
Out[2]: <Article: Article object>

{% endhighlight %}

Попробуем сделать сравнение

{% highlight python %}

In [3]: from django.db.models import F

In [4]: Article.objects.filter(number_of_likes__gte=F('count'))
Out[4]: [<Article: Article object>]

{% endhighlight %}


Посмотрим какой SQL запрос был сгенерирован

{% highlight python %}

In [5]: print Article.objects.filter(number_of_likes__gte=F('count')).query
SELECT "example_article"."id", "example_article"."content", "example_article"."count", "example_article"."number_of_likes" FROM "example_article" WHERE "example_article"."number_of_likes" >= ("example_article"."count")

{% endhighlight %}

Если вам интересно узнать как работают F выражения изнутри советую прочитать старенькую [статью Ивана Сагалаева](http://softwaremaniacs.org/blog/2008/11/21/expressions-in-django-queries/).
