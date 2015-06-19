---
layout: post
title: Добавляем ошибки в форму минуя метод clean
tags: "python, django"
category: ru
---

Иногда бывает удобно добавлять ошибки полей формы минуя метод clean. Для этого в Django > 1.7 был добавлен новый метод add_error в экземпляр формы. Использовать этот метод легко, достаточно указать в качестве его параметра id поля и сообщение об ошибке, после чего вернуть form_invalid. Пример использования в FormView:

{% highlight python %}
class TestFormView(FormView):
    form_class = TestForm
    template_name = 'test/form.html'

    def form_valid(self, form):
        less_than_one = form.cleaned_data.get('less_than_one')
        if less_than_one > 1:
            form.add_error('less_than_one', forms.ValidationError('Can not be greater than one'))
            return super(TestFormView, self).form_invalid(form)
        return super(TestFormView, self).form_valid(form)

{% endhighlight %}

Если по каким то причинам вы не в состоянии обновиться до Django > 1.7, есть вариант воспользоваться следующим приемом:

{% highlight python %}
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
 
class AddErrorMixin(object):
    "Backport add_error() for django <1.7"
    def add_error(self, field, msg):
        field = field or NON_FIELD_ERRORS
        if field in self._errors:
            self._errors[field].append(msg)
        else:
            self._errors[field] = self.error_class([msg])
 
class ExampleForm(AddErrorMixin, forms.Form):
    pass
{% endhighlight %}
