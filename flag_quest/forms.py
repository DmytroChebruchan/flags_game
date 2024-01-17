from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    options = []

    class Meta:
        model = Answer
        fields = ["flag_picture", "your_answer"]

    def __init__(self, options=None, *args, **kwargs):
        if options:
            self.options = options
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields["selected_country"] = forms.ChoiceField(
            choices=self.options,
            widget=forms.RadioSelect(),
            required=True,
        )
