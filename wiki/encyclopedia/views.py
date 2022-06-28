from cProfile import label
from django.shortcuts import render
from django import forms
from . import util
from django.shortcuts import redirect
import random
from random import *

class TaskForm(forms.Form):
    title = forms.CharField(label="Title");
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'content', "style":"height: 20vh; width:100%"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def createnew(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/createnew.html", {
                    "form": form,
                    "exists": True
                })
            else: 
                util.save_entry(title, content)
                return redirect('entry', title)
        else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "encyclopedia/createnew.html", {
                    "form": form,
                    "exists": False
                }) 

    return render(request, "encyclopedia/createnew.html", {
        "form": TaskForm(),
        "exists": False
    });

def edit(request, title):
    
    content = util.get_entry(title)
    form = TaskForm({"content": content, "title":title})
        
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry', title)
        else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "tasks/edit.html", {
                    "form": form,
                    "title": title
                })

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
        })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "info": util.get_entry(title),
        "title": title
    })

def search(request):
    title = request.GET.get('q')
    print(title)
    if util.get_entry(title) == None:
       list = util.list_entries()
       filteredList = filter(lambda el: title in el, list)
       return render(request, "encyclopedia/listentries.html", {
        "entries": filteredList
    }) 
    else:
        return render(request, "encyclopedia/entry.html", {
            "info": util.get_entry(title),
            "title": title
        })

def random(request):
       list = util.list_entries()
       listLen = len(list)-1
       value = randint(0, listLen)
       title = list[value]
       return render(request, "encyclopedia/entry.html", {
        "info":  util.get_entry(title),
        "title": title
        })

def error_404_view(request, exception):
    return render(request, 'error.html')

