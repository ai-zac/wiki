from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_preview(request, title):
    entry = util.get_entry(title)
    if entry is None:
        context = {"code": 404, "description": "Entry not found"}
        body = render(request, "encyclopedia/error.html", context)
        return HttpResponseNotFound(body)

    context = {"title": title, "content": markdown(entry)}
    return render(request, "encyclopedia/entry.html", context)


@require_GET
def search(request):
    r = request.GET.copy()
    q = r["q"]
    entries = util.list_entries()
    s = [m for m in entries if q in m]

    if len(s):
        return redirect("entry", title=s[0])
    return render(request, "encyclopedia/index.html", {"entries": s})


def create_entry(request):
    return render(request, "encyclopedia/create.html", {})
