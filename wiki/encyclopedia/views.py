from django.shortcuts import render, redirect

from . import util
import random
import markdown2

def convert_md_to_html(title):
    content = util.get_entry(title)
    #create object of type Markdown
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encylopedia/error.html",{
            "message":"This entry does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        html_content = convert_md_to_html(query)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": html_content
        })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if query.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html",{
                "recommendation":recommendation,
                "query":query
            })
           

def newEntry(request):
    if request.method == "POST":
        #get info from HTML form -> comes from "name" attribute
        title = request.POST.get("title")
        content = request.POST.get("entryText")

        # Check if entry already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": f'An entry with the title "{title}" already exists. Please edit the already existing entry or choose another topic'
            })

        # Save the new entry
        util.save_entry(title, content)
        html_content=convert_md_to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })

    # GET request → show the empty form if nothing entered
    return render(request, "encyclopedia/newEntry.html")

def editEntry(request,title):
    if request.method=="GET":
        content=util.get_entry(title)
        if content is None:
            return render(request,"enyclopedia/error",{
                "message":f"The entry '{title}' does not exist."
            })
        return render(request,"encyclopedia/editEntry.html",{
            "title":title,
            "content":content
        })
    elif request.method=="POST":
        new_content=request.POST.get("entryText")
        util.save_entry(title,new_content)
        return redirect("entry", title=title)




def randomPage(request):
    #util.list_entries() returns a list with the names of all entries (.md is stripped)
    entryList = util.list_entries()
    randomEntry = random.choice(entryList)
    #takes the url-pattern "entry" and adds the title randomEntry
    return redirect("entry",title=randomEntry)


