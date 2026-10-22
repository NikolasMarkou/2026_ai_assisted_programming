# E6 Spec: notes service, then one function

## Part 1: the service

Build a small notes service in one file, `service.py`, with the Python standard library
only (`http.server` and `json`). It starts with `python3 service.py --port 8000`, listens
on `127.0.0.1` only, keeps its notes in memory and speaks JSON. It has 4 endpoints:

| Endpoint | Request | Reply |
|---|---|---|
| `POST /notes` | JSON body `{"text": "..."}` | 201 and `{"id": 1, "text": "..."}`; ids start at 1 and go up by 1; 400 if `text` is missing or not a string |
| `GET /notes` | none | 200 and a JSON list of all notes, oldest first |
| `GET /notes/<id>` | none | 200 and the note, or 404 if the id does not exist |
| `DELETE /notes/<id>` | none | 204 with no body, or 404 if the id does not exist |

Do not add any package that is not in the standard library. Ask before you add one.

## Part 2: one function

Open `duration.py`. It has a signature, a docstring and 3 examples, and no body. Let the
agent write the body. The examples are doctests, so they run with:

```text
python3 -m doctest duration.py
```

No output means every example passed.
