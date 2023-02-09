from django.shortcuts import render, get_object_or_404
from map.models import Map


def home(request):
    objects = Map.objects.all()
    return render(request, "home.html", {"maps": objects})


def detail(request, detail_id):
    object = get_object_or_404(Map, pk=detail_id)
    return render(request, "map_detail.html", {"map": object})
