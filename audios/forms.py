from django import forms

from audios.models import Audio


class AudioForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    audio_file = forms.FileField()

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 34:
            raise forms.ValidationError("Length of title must be smaller then 34 char")
        return title
    
    def clean_author(self):
        author = self.cleaned_data["author"]
        if len(author) > 30:
            raise forms.ValidationError("Length of author must be smaller then 20 char")
        return author
    
    # class Meta:
    #     db_table = Audio
    #     fields = ["title", "author", "audio_file"]