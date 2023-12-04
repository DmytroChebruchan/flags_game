from django import forms

from .models import CountryInfo


class FlagForm(forms.ModelForm):
    options = []

    class Meta:
        model = CountryInfo
        fields = []

    def __init__(self, options=None, *args, **kwargs):
        self.options = options if options else []
        super(FlagForm, self).__init__(*args, **kwargs)
        self.fields["selected_country"] = forms.ChoiceField(
            choices=self.options + [("unknown", "I do not know")],
            widget=forms.RadioSelect(),
            required=True,
        )
