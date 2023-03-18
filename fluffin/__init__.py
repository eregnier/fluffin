import http.server
import json
import os
import sys
import shutil
import socketserver
import threading
import time
import traceback

from jinja2 import Environment, FileSystemLoader
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

BASE_PATH = os.getcwd()
TEMPLATE_DIR = BASE_PATH + "/templates"
DIST_DIR = BASE_PATH + "/dist"
PAGES_DIR = TEMPLATE_DIR + "/pages"
STATIC_DIR = TEMPLATE_DIR + "/static"
template_paths = [
    TEMPLATE_DIR + "/pages",
    TEMPLATE_DIR + "/partials",
    TEMPLATE_DIR + "/layouts",
    TEMPLATE_DIR + "/static",
]
jinja_paths = FileSystemLoader(template_paths)

env = Environment(
    loader=jinja_paths, autoescape=True, trim_blocks=True, lstrip_blocks=True
)

hot_reload_js = """
window.addEventListener('load', () => {
    setInterval(() => {
        fetch("/last-update-date.json").then(response => {
            return response.json()
        }).then(data => {
            if (data.timestamp > + new Date() - 1501) {
                window.location = window.location.href
            }
        })
    }, 1500);
})
"""


def init():
    for folder in template_paths + [TEMPLATE_DIR]:
        if not os.path.isdir(folder):
            os.makedirs(folder)
    hot_reload_path = f"{TEMPLATE_DIR}/static/hot-reload.js"
    if not os.path.isfile(hot_reload_path):
        with open(hot_reload_path, "w") as f:
            f.write(hot_reload_js)


def debounce(s):
    def decorate(f):
        t = None

        def wrapped(*args, **kwargs):
            nonlocal t
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = f(*args, **kwargs)
                t = time.time()
                return result

        return wrapped

    return decorate


def render_template(template_name):
    print(f"> Rendering {template_name}")
    template = env.get_template(template_name)
    output = template.render()
    dist_file = os.path.join(DIST_DIR, template_name)
    with open(dist_file, "w") as f:
        f.write(output)
    print(f"Rendered {template_name}")


@debounce(0.3)
def render_templates():
    rendered = False
    while not rendered:
        try:
            try_render_templates()
            rendered = True
        except Exception as e:
            print(traceback.format_exc())
            print("\n > Error rendering templates, retrying in 5 seconds")
            rendered = False
            time.sleep(5)


def try_render_templates():
    print("\n => Generating <=\n")
    if os.path.isdir(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)
    shutil.copytree(f"{TEMPLATE_DIR}/static", f"{DIST_DIR}/static")
    if not os.path.exists(os.path.join(DIST_DIR, "static")):
        os.makedirs(os.path.join(DIST_DIR, "static"))
    for filename in os.listdir(PAGES_DIR):
        if filename.endswith(".html"):
            render_template(filename)
    with open(f"{DIST_DIR}/last-update-date.json", "w") as f:
        f.write(json.dumps({"timestamp": int(time.time() * 1000)}))


class FileWatcherHandler(threading.Thread):
    def __init__(self, web_server_thread):
        super().__init__()
        self.ready = True
        self.web_server_thread = web_server_thread

    def stop_watch(self):
        self.ready = False

    def run(self):
        event_handler = Event(web_server_thread=self.web_server_thread)
        observer = Observer()

        print("\n + Watching for changes...", TEMPLATE_DIR)
        observer.schedule(event_handler, TEMPLATE_DIR, recursive=True)
        observer.start()
        while self.ready:
            time.sleep(0.2)
        observer.stop()
        observer.join()


class Event(LoggingEventHandler):
    def __init__(self, *args, **kwargs):
        self.web_server_thread = kwargs.pop("web_server_thread")
        super().__init__(*args, **kwargs)

    def on_modified(self, event):
        self.web_server_thread.stop_server()
        rendered = False
        render_templates()
        self.web_server_thread.start_server()


class WebServerHandler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.port = 8110
        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), handler)
        self.ready = True
        self.active = True
        print(f" + Listening http://localhost:{self.port}")

    def run(self):
        while self.active:
            if self.ready:
                os.chdir(DIST_DIR)
                try:
                    self.httpd.serve_forever()
                except:
                    time.sleep(0.2)
            else:
                time.sleep(0.2)

    def stop_server(self):
        self.ready = False
        self.httpd.shutdown()

    def close(self):
        self.active = False
        self.stop_server()
        self.httpd.server_close()

    def start_server(self):
        self.ready = True


help_string = """
fluffin help:

    fluffin --dev : start dev server
    fluffin : build only
"""


def run():

    if "--help" in os.sys.argv:
        print(help_string)
        sys.exit(0)

    init()
    render_templates()

    if "--dev" in os.sys.argv:
        web_server_thread = WebServerHandler()
        watch_thread = FileWatcherHandler(web_server_thread=web_server_thread)
        try:
            web_server_thread.start()
            watch_thread.start()
            while True:
                time.sleep(0.2)
        except KeyboardInterrupt:
            print(" > stopping server...")
            web_server_thread.close()
            watch_thread.stop_watch()
            web_server_thread.join()
            watch_thread.join()
            time.sleep(0.5)
            print(" ✖ Stopped dev server. Bye!")
    else:
        with open(f"{DIST_DIR}/static/hot-reload.js", "w") as f:
            f.write("//no hot reload in production")

if __name__ == "__main__":
    run()
