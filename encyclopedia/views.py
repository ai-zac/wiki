from random import choice
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from markdown2 import markdown

from . import util


@require_GET
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


@require_GET
def entry_preview(request, title):
    entry = util.get_entry(title)
    if entry is None:
        context = {"code": 404, "description": "Entry not found"}
        body = render(request, "encyclopedia/error.html", context)
        return HttpResponseNotFound(body)

    return render(
        request, "encyclopedia/entry.html", {"title": title, "content": markdown(entry)}
    )


@require_GET
def search(request):
    p = request.GET.copy()
    q = p["q"]
    entries = util.list_entries()
    s = [m for m in entries if q in m]

    if len(s):
        return redirect("entry", title=s[0])
    return render(request, "encyclopedia/index.html", {"entries": s})


@require_http_methods(["GET", "POST"])
def create_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        r = request.POST.copy()
        entries = util.list_entries()
        if r["title"] in entries:
            context = {"code": 400, "description": "Bad request, entry already exists"}
            body = render(request, "encyclopedia/error.html", context)
            return HttpResponseNotFound(body)

        util.save_entry(r["title"], r["content"])
        return redirect("entry", title=r["title"])


@require_http_methods(["GET", "POST"])
def edit_entry(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)

        return render(
            request, "encyclopedia/edit.html", {"title": title, "body": entry}
        )
    else:
        r = request.POST.copy()
        util.save_entry(title, r["content"])
    return redirect("entry", title=title)


@require_GET
def random_entry(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect("entry", title=entry)
