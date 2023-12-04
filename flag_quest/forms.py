from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['flag_picture', 'your_answer']

    def __init__(self, options=None, flag=None, *args, **kwargs):
        self.options = options if options else []
        self.flag = flag if flag else ''
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields["your_answer"] = forms.ChoiceField(
            choices=self.options,
            widget=forms.RadioSelect(),
            required=True,
        )
