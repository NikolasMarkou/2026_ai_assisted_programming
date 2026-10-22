"""Check a notes-service scaffold: standard-library imports, then the 4 endpoints.

Usage: python3 check_scaffold.py [DIRECTORY] [--entry service.py] [--wait 5]
Starts `python3 ENTRY --port PORT` in DIRECTORY on a free loopback port, calls the 4
endpoints of spec.md and prints PASS or FAIL for the imports and for each endpoint.
Exit code 0 when the imports and all 4 endpoints pass, 1 otherwise.
Standard library only.
"""
import argparse
import ast
import http.client
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

ENDPOINTS = ("POST /notes", "GET /notes", "GET /notes/<id>", "DELETE /notes/<id>")


def third_party_imports(folder):
    """List of 'file: module' for every import that is not standard library or local.

    folder: a Path. Reads every .py file in it; a name equal to another .py file in the
    folder counts as local. A file that does not parse is listed as a syntax error.
    """
    local = {p.stem for p in folder.glob("*.py")}
    found = []
    for path in sorted(folder.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as error:
            found.append(f"{path.name}: syntax error line {error.lineno}")
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            for name in names:
                top = name.split(".")[0]
                if top not in sys.stdlib_module_names and top not in local:
                    found.append(f"{path.name}: {name}")
    return found


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def wait_for_port(port, process, seconds):
    """True when something accepts a connection on the port; False if the process
    exits first or the time runs out."""
    end = time.time() + seconds
    while time.time() < end and process.poll() is None:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            return True
        except OSError:
            time.sleep(0.1)
    return False


def call(port, method, path, body=None):
    """One HTTP request. Returns (status, parsed JSON or None). Raises OSError."""
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
    data = None if body is None else json.dumps(body).encode()
    connection.request(method, path, body=data,
                       headers={"Content-Type": "application/json"})
    reply = connection.getresponse()
    raw = reply.read()
    connection.close()
    try:
        return reply.status, json.loads(raw) if raw else None
    except ValueError:
        return reply.status, None


def check_post(port):
    status, note = call(port, "POST", "/notes", {"text": "first"})
    if (status, note) != (201, {"id": 1, "text": "first"}):
        return f"POST valid body: got {status} {note}"
    status, note = call(port, "POST", "/notes", {"text": "second"})
    if (status, note) != (201, {"id": 2, "text": "second"}):
        return f"second POST: got {status} {note}"
    status, _ = call(port, "POST", "/notes", {"other": 1})
    return "" if status == 400 else f"POST without text: got {status}, want 400"


def check_list(port):
    status, notes = call(port, "GET", "/notes")
    want = [{"id": 1, "text": "first"}, {"id": 2, "text": "second"}]
    return "" if (status, notes) == (200, want) else f"got {status} {notes}"


def check_get(port):
    status, note = call(port, "GET", "/notes/2")
    if (status, note) != (200, {"id": 2, "text": "second"}):
        return f"GET /notes/2: got {status} {note}"
    status, _ = call(port, "GET", "/notes/99")
    return "" if status == 404 else f"GET unknown id: got {status}, want 404"


def check_delete(port):
    status, _ = call(port, "DELETE", "/notes/1")
    if status != 204:
        return f"DELETE /notes/1: got {status}, want 204"
    if call(port, "GET", "/notes/1")[0] != 404:
        return "a deleted note can still be read"
    status, _ = call(port, "DELETE", "/notes/99")
    return "" if status == 404 else f"DELETE unknown id: got {status}, want 404"


CHECKS = (check_post, check_list, check_get, check_delete)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("directory", nargs="?", default=".")
    parser.add_argument("--entry", default="service.py")
    parser.add_argument("--wait", type=float, default=5.0, help="seconds to wait")
    args = parser.parse_args()
    folder = Path(args.directory).resolve()
    outside = third_party_imports(folder)
    if outside:
        print("FAIL  imports: dependencies you did not approve: " + ", ".join(outside))
    else:
        print("PASS  imports: standard library only")
    port = free_port()
    command = [sys.executable, args.entry, "--port", str(port)]
    process = subprocess.Popen(command, cwd=folder, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, text=True)
    problems = []
    try:
        if wait_for_port(port, process, args.wait):
            for name, check in zip(ENDPOINTS, CHECKS):
                try:
                    problems.append(check(port))
                except OSError as error:
                    problems.append(f"request failed: {error}")
        else:
            exited = process.poll() is not None
            reason = "the process exited" if exited else "nothing listens"
            print(f"FAIL  start: {reason} on 127.0.0.1:{port}")
            problems = ["service not running"] * len(ENDPOINTS)
    finally:
        process.kill()
        error_text = process.stderr.read().strip().splitlines()[-3:]
        process.wait()
    for name, problem in zip(ENDPOINTS, problems):
        detail = f": {problem}" if problem else ""
        print(f"{'FAIL' if problem else 'PASS'}  {name}{detail}")
    for line in error_text if any(problems) else []:
        print(f"      service stderr: {line}")
    passed = sum(not problem for problem in problems)
    print(f"{passed} of {len(ENDPOINTS)} endpoints pass")
    return 0 if passed == len(ENDPOINTS) and not outside else 1


if __name__ == "__main__":
    sys.exit(main())
