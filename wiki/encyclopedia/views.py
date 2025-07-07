from django.shortcuts import render, redirect

from . import util
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    #markdown_content = util.get_entry(title)
    #html_content = markdown2.markdown(markdown_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
        #"content":html_content
    })


def newEntry(request):
    if request.method == "POST":
        #get info from HTML form -> comes from "name" attribute
        title = request.POST.get("title")
        content = request.POST.get("entryText")

        # Check if entry already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/newEntry.html", {
                "error": f'An entry with the title "{title}" already exists. Please edit the already existing entry or choose another topic'
            })

        # Save the new entry
        util.save_entry(title, content)
        return redirect("entry", title=title)

    # GET request → show the empty form if nothing entered
    return render(request, "encyclopedia/newEntry.html")

def editEntry(request,title):
    if request.method =="GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/editEntry.html", {
            "title": title,
            "content": content
        })
    elif request.method == "POST":
        content = request.POST.get("entryText")
        # Save the new entry
        util.save_entry(title, content)
        return redirect("entry", title=title)

def randomPage(request):
    #util.list_entries() returns a list with the names of all entries (.md is stripped)
    entryList = util.list_entries()
    randomEntry = random.choice(entryList)
    #takes the url-pattern "entry" and adds the title randomEntry
    return redirect("entry",title=randomEntry)

def search(request,title):
    allEntries = util.list_entries()
    if(title in allEntries):
        return redirect("entry", title = title)
    
