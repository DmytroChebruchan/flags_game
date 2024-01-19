from django import forms
from django.forms import RadioSelect

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("your_answer", "flag_picture")

    def set_params(self, question_set):
        self.set_answer_options(question_set)
        self.set_flag_field()
        self.set_country_item(question_set)

    def set_answer_options(self, question_set):
        options = question_set.get("options", []) if question_set else []
        self.fields["your_answer"] = forms.ChoiceField(
            choices=options, widget=RadioSelect()
        )

    def set_flag_field(self):
        self.fields["flag_picture"].widget = forms.HiddenInput()
        self.fields["flag_picture"].label = ""

    def set_country_item(self, question_set):
        country_item = question_set.get("countries_item")
        self.fields["flag_picture"].initial = country_item
