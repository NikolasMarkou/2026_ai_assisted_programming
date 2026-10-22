"""Bookmarks: a small library and command line. The data is one JSON file.

    python3 bookmarks.py --file marks.json add URL TITLE [--tag TAG ...]
    python3 bookmarks.py --file marks.json list
    python3 bookmarks.py --file marks.json remove ID
    python3 bookmarks.py --file marks.json list [--tag TAG]
    python3 bookmarks.py --file marks.json search WORD
    python3 bookmarks.py --file marks.json export --format md
Reference solution with all 4 backlog features.
"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def load(path):
    """Return the list of bookmarks in the file, or [] when the file does not exist."""
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save(path, items):
    Path(path).write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")


def add(items, url, title, tags=()):
    """Append a bookmark with the next free id and return it."""
    new_id = max((item["id"] for item in items), default=0) + 1
    item = {"id": new_id, "url": url, "title": title, "tags": list(tags)}
    items.append(item)
    return item


def remove(items, item_id):
    """Delete the bookmark with this id. Returns True when one was removed."""
    kept = [item for item in items if item["id"] != item_id]
    removed = len(kept) != len(items)
    items[:] = kept
    return removed


def normalize(url):
    """The URL with scheme and host in lower case, one final / and the fragment cut."""
    parts = urlsplit(url)
    path = parts.path[:-1] if parts.path.endswith("/") else parts.path
    host = parts.netloc.lower()
    return urlunsplit((parts.scheme.lower(), host, path, parts.query, ""))


def find_duplicate(items, url):
    """Return the saved bookmark with the same normalized URL, or None."""
    return next((i for i in items if normalize(i["url"]) == normalize(url)), None)


def search(items, word):
    """Bookmarks whose title or URL contains word: title matches first, each by id."""
    word = word.lower()
    in_title = [i for i in items if word in i["title"].lower()]
    in_url = [i for i in items if word in i["url"].lower() and i not in in_title]
    return in_title + in_url


def to_markdown(items):
    lines = []
    for item in items:
        tags = f" [{', '.join(item['tags'])}]" if item["tags"] else ""
        lines.append(f"- [{item['title']}]({item['url']}){tags}")
    return lines


def format_item(item):
    tags = f" [{', '.join(item['tags'])}]" if item["tags"] else ""
    return f"{item['id']}. {item['title']} <{item['url']}>{tags}"


def build_parser():
    parser = argparse.ArgumentParser(prog="bookmarks.py")
    parser.add_argument("--file", default="bookmarks.json")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("add")
    one.add_argument("url")
    one.add_argument("title")
    one.add_argument("--tag", action="append", default=[])
    sub.add_parser("list").add_argument("--tag")
    sub.add_parser("remove").add_argument("id", type=int)
    sub.add_parser("search").add_argument("word")
    sub.add_parser("export").add_argument("--format", required=True, choices=["md"])
    return parser


def main(argv, out=sys.stdout):
    args = build_parser().parse_args(argv)
    items = load(args.file)
    if args.command == "add":
        saved = find_duplicate(items, args.url)
        if saved:
            print(f"already saved: {saved['id']}", file=out)
            return 1
        item = add(items, args.url, args.title, args.tag)
        save(args.file, items)
        print(f"saved {item['id']}", file=out)
    elif args.command == "list":
        wanted = args.tag.lower() if args.tag else None
        for item in items:
            if wanted is None or wanted in [tag.lower() for tag in item["tags"]]:
                print(format_item(item), file=out)
    elif args.command == "search":
        for item in search(items, args.word):
            print(format_item(item), file=out)
    elif args.command == "export":
        for line in to_markdown(items):
            print(line, file=out)
    elif remove(items, args.id):
        save(args.file, items)
        print(f"removed {args.id}", file=out)
    else:
        print(f"no bookmark {args.id}", file=out)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
