import csv
import json
import os
import uuid

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item


def home(request):
    items = Item.objects.all().order_by('-created_at')

    total = items.count()
    lost = items.filter(status='LOST').count()
    found = items.filter(status='FOUND').count()
    resolved = items.filter(status='RESOLVED').count()

    context = {
        "total": total,
        "lost": lost,
        "found": found,
        "resolved": resolved,
        "recent_items": items[:10],
    }

    return render(request, "pages/home.html", context)


def items(request):
    all_items = Item.objects.all().order_by('-created_at')

    # simple search/filter using GET params
    query = request.GET.get("q", "").strip().lower()
    status_filter = request.GET.get("status", "").strip()

    if query:
        all_items = all_items.filter(title__icontains=query) | all_items.filter(location__icontains=query)

    if status_filter:
        all_items = all_items.filter(status=status_filter)

    context = {
        "all_items": all_items,
        "query": query,
        "status_filter": status_filter,
    }

    return render(request, "pages/items.html", context)


@login_required(login_url='login')
def report(request):
    if request.method == "POST":
        new_item = Item(
            title=request.POST.get("title", "").strip(),
            status=request.POST.get("status", "LOST"),
            category=request.POST.get("category", "").strip(),
            location=request.POST.get("location", "").strip(),
            date=request.POST.get("date", ""),
            description=request.POST.get("description", "").strip(),
            contact=request.POST.get("contact", "").strip(),
        )

        # handle uploaded image
        image_file = request.FILES.get('image') if hasattr(request, 'FILES') else None
        if image_file:
            new_item.image = image_file

        new_item.save()

        return redirect("items")

    return render(request, "pages/report.html")


def detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        item = None

    context = {
        "item": item,
        "item_id": item_id,
    }

    return render(request, "pages/detail.html", context)


@login_required(login_url='login')
def delete_item(request, item_id):
    if request.method == "POST":
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
        except Item.DoesNotExist:
            pass

    return redirect("items")


@login_required(login_url='login')
def edit_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return redirect("items")

    if request.method == "POST":
        item.title = request.POST.get("title", "").strip()
        item.status = request.POST.get("status", "LOST")
        item.category = request.POST.get("category", "").strip()
        item.location = request.POST.get("location", "").strip()
        item.date = request.POST.get("date", "")
        item.description = request.POST.get("description", "").strip()
        item.contact = request.POST.get("contact", "").strip()

        # handle uploaded image replacement
        image_file = request.FILES.get('image') if hasattr(request, 'FILES') else None
        if image_file:
            item.image = image_file

        item.save()

        return redirect("detail", item_id=item_id)

    context = {
        "item": item,
        "item_id": item_id,
    }

    return render(request, "pages/edit.html", context)
