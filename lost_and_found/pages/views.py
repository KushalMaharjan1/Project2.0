import csv
import json

from django.shortcuts import render, redirect

CSV_FILE = "data/lost_found.csv"
JSON_FILE = "data/lost_found.json"

FIELDNAMES = ["title", "status", "category", "location", "date", "description", "contact"]


def read_items():
    items = []
    try:
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(row)
    except FileNotFoundError:
        print("No records file yet.")
    return items


def write_items(items):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


def sync_json(items):
    with open(JSON_FILE, "w") as file:
        json.dump(items, file, indent=4)


def read_json():
    items = []
    try:
        with open(JSON_FILE, "r") as file:
            items = json.load(file)
    except FileNotFoundError:
        print("No JSON records file yet.")
    return items


def home(request):
    items = read_items()

    total = len(items)
    lost = 0
    found = 0
    resolved = 0

    for item in items:
        if item["status"] == "LOST":
            lost = lost + 1
        elif item["status"] == "FOUND":
            found = found + 1
        elif item["status"] == "RESOLVED":
            resolved = resolved + 1

    context = {
        "total": total,
        "lost": lost,
        "found": found,
        "resolved": resolved,
        "recent_items": items,
    }

    return render(request, "pages/home.html", context)


def items(request):
    all_items = read_items()

    # simple search/filter using GET params
    query = request.GET.get("q", "").strip().lower()
    status_filter = request.GET.get("status", "").strip()

    if query:
        all_items = [
            item for item in all_items
            if query in item["title"].lower() or query in item["location"].lower()
        ]

    if status_filter:
        all_items = [item for item in all_items if item["status"] == status_filter]

    context = {
        "items": list(enumerate(all_items)),
        "query": query,
        "status_filter": status_filter,
    }

    return render(request, "pages/items.html", context)


def report(request):
    if request.method == "POST":
        new_item = {
            "title": request.POST.get("title", "").strip(),
            "status": request.POST.get("status", "LOST"),
            "category": request.POST.get("category", "").strip(),
            "location": request.POST.get("location", "").strip(),
            "date": request.POST.get("date", "").strip(),
            "description": request.POST.get("description", "").strip(),
            "contact": request.POST.get("contact", "").strip(),
        }

        all_items = read_items()
        all_items.append(new_item)
        write_items(all_items)
        sync_json(all_items)

        return redirect("items")

    return render(request, "pages/report.html")


def detail(request, item_id):
    all_items = read_items()

    item = None
    if 0 <= item_id < len(all_items):
        item = all_items[item_id]

    context = {
        "item": item,
        "item_id": item_id,
    }

    return render(request, "pages/detail.html", context)


def delete_item(request, item_id):
    if request.method == "POST":
        all_items = read_items()
        if 0 <= item_id < len(all_items):
            all_items.pop(item_id)
            write_items(all_items)
            sync_json(all_items)

    return redirect("items")


def edit_item(request, item_id):
    all_items = read_items()

    if not (0 <= item_id < len(all_items)):
        return redirect("items")

    if request.method == "POST":
        updated_item = {
            "title": request.POST.get("title", "").strip(),
            "status": request.POST.get("status", "LOST"),
            "category": request.POST.get("category", "").strip(),
            "location": request.POST.get("location", "").strip(),
            "date": request.POST.get("date", "").strip(),
            "description": request.POST.get("description", "").strip(),
            "contact": request.POST.get("contact", "").strip(),
        }

        all_items[item_id] = updated_item
        write_items(all_items)
        sync_json(all_items)

        return redirect("detail", item_id=item_id)

    context = {
        "item": all_items[item_id],
        "item_id": item_id,
    }

    return render(request, "pages/edit.html", context)
