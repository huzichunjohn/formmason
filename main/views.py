# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import ListView

from main.models import FormSchema, FormResponse

class HomePageView(ListView):
    model = FormSchema
    template_name = "home.html"

class CustomFormView(FormView):
    template_name = "custom_form.html"

    def get_form(self):
        form_structure = FormSchema.objects.get(pk=self.kwargs["form_pk"]).schema

        custom_form = forms.Form(**self.get_form_kwargs())
        for key, value in form_structure.items():
            field_class = self.get_field_class_from_type(value)
            if field_class is not None:
                custom_form.fields[key] = field_class()
            else:
                raise TypeError("Invalid field type {}".format(value))
        return custom_form

    def get_field_class_from_type(self, value_type):
        if value_type == "string":
            return forms.CharField
        elif value_type == "number":
            return forms.IntegerField
        else:
            return None

    def form_valid(self, form):
        custom_form = FormSchema.objects.get(pk=self.kwargs["form_pk"])
        user_response = form.cleaned_data

        form_response = FormResponse(form=custom_form, response=user_response)
        form_response.save()

        return HttpResponseRedirect(reverse('home'))
