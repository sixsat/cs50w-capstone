from django import forms


class NewResourceForm(forms.Form):
    attrs = {
        "autocomplete": "off",
        "class": "form-control"
    }
    CATEGORY_CHOICES = [
        ("BOOK", "Book"),
        ("CODE", "Code"),
        ("CRS", "Course"),
        ("DOC", "Document"),
        ("QUIZ", "Quiz"),
        ("VID", "Video")
    ]
    LANGUAGE_CHOICES = [
        (1, "CSS"),
        (2, "HTML"),
        (3, "JavaScript"),
        (4, "Python")
    ]
    LEVEL_CHOICES = [
        ("INTR", "Introductory"),
        ("MEDI", "Intermediate"),
        ("ADVC", "Advanced")
    ]

    title = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs=attrs), label="Title"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs=attrs), label="Description"
    )
    url = forms.URLField(
        max_length=255, widget=forms.TextInput(attrs=attrs), label="URL"
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES, widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ), label="Category"
    )
    language = forms.MultipleChoiceField(
        choices=LANGUAGE_CHOICES, widget=forms.SelectMultiple(
            attrs={
                "class": "form-select"
            }
        ), label="Language (CTRL + click to select more than one)"
    )
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES, widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ), label="Level"
    )