---
layout: post
title: Несколько полезных практик использования запросов в Django ORM
tags: "python, django"
category: ru
---

# select_related()

Метод select_related() создает запрос, который объединяет связанные объекты. Метод не выполняет дополнительные запросы при доступе к связанным объектам, что может увеличить производительность, но при этом увеличивается объем получаемых данных. Я думаю было бы целесообразно использовать select_related() вместе с методом iterator(), так мы сможем получать большие данные по кусочкам не засоряя память:

{% highlight python %}
users = User.objects.select_related().all()

for user in users.iterator():
    ...
{% endhighlight %}

# exists()

Давайте рассмотрим небольшой практический пример:

{% highlight python %}
# Запрос выполняться не будет
users_at_city = User.objects.filter(city='Somecity')

# Тут уже выполнится запрос
if users_at_city:
    ...
{% endhighlight %}

Строка с оператором if выполнит запрос QuerySet, даже если вы никогда не собираетесь использовать результаты данного запроса. Для этих целей было бы целесообразно воспользоваться методом exists():

{% highlight python %}
users_at_city = User.objects.filter(city='Somecity')

if users_at_city.exists():
    ...
{% endhighlight %}

# Комбинирование методов exists() и iterator()

Комбинирование двух этих методов позволит нам:

1. Проверить существуют ли записи в таблице без получения этих данных (exists)
2. Если записи существуют, получить их порциями (iterator)

Пример:

{% highlight python %}
users = User.objects.all()
if users.exists():
    for user in users.iterator():
        ...
{% endhighlight %}

По мотивам статьи: http://blog.etianen.com/blog/2013/06/08/django-querysets/
