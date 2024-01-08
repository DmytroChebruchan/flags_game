from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    options = []

    class Meta:
        model = Answer
        fields = ["flag_picture", "your_answer"]

    def __init__(self, options=None, *args, **kwargs):
        self.options = options if options else []
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields["selected_country"] = forms.ChoiceField(
            choices=self.options + [("unknown", "I do not know")],
            widget=forms.RadioSelect(),
            required=True,
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
