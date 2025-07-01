from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
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