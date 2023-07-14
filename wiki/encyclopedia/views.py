import markdown2
from random import choice
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from .util import get_entry, list_entries, save_entry


class TitleForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text", widget=forms.Textarea)


class EditForm(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        placeholder_text = kwargs.pop('placeholder_text', None)
        super().__init__(*args, **kwargs)
        self.fields['text'].initial = placeholder_text


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if get_entry(title) is not None:
        f = get_entry(title)
    else:
        return render(request, "encyclopedia/erro.html", {
            "message": "requested page was not found",
        })
    text = f
    text = (markdown2.markdown(text))
    return render(request, "encyclopedia/wiki.html", {
        "text": text,
        "title": title
        # name.capitalize()
    })


def search(request):
    q = request.GET.get('q', '')
    if get_entry(q) is not None:
        return wiki(request, q)
    else:
        arr = []
        for entrie in list_entries():
            if q.upper() in entrie.upper():
                arr.append(entrie)
        return render(request, "encyclopedia/search.html", {
            "arr": arr,

        })


def newPage(request):
    if request.method == "POST":
        form = TitleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            for entry in list_entries():
                if entry.upper() == title.upper():
                    return render(request, "encyclopedia/erro.html", {
                        "message": "This encyclopedia entry already exists with the provided title."
                    })
            save_entry(title, text)
            print(title)
            return HttpResponseRedirect(reverse('wiki', kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/newPage.html", {
                "formTitle": form
            })
    return render(request, "encyclopedia/newPage.html", {
        "formTitle": TitleForm(),
    })


def editPage(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            save_entry(title, text)
            print(title)
            return HttpResponseRedirect(reverse('wiki', kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/editPage.html", {
                "title": title,
                "formEdit": form,
            })
    else:
        if title is None:
            return render(request, "encyclopedia/erro.html", {
                "message": "Unexpected error"
            })
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "formEdit": EditForm(placeholder_text=get_entry(title)),
        })


def random(request):
    name = choice(list_entries())
    return wiki(request, name)
