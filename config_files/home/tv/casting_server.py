#!/usr/bin/python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import hashlib
import subprocess as sp
import os

env = os.environ.copy()
env["WAYLAND_DISPLAY"] = "wayland-1"

MACHINE_ID_PATH = "/etc/machine-id"
EXTRA_SECRET_PATH = "/home/tv/extra_secret.txt"

with open(MACHINE_ID_PATH, 'r') as file:
    machine_id = file.read()
extra = ""
if os.path.exists(EXTRA_SECRET_PATH):
    with open(EXTRA_SECRET_PATH) as file:
        extra = file.read()
secret = hashlib.sha256((machine_id + extra + "earlcasting").encode()).hexdigest()
print("Secret for checksum:", secret)

def clean_url(url):
  # I want no funny business in my URLs
  allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:-_/#&?=.,"
  for char in url:
      if char not in allowed_chars:
          raise ValueError(f"Invalid character found: {char}")
  if len(url) > 300:
          raise ValueError(f"Too long URL")
  return url


class CastingHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    checksum = self.path[1: (64 + 1)]
    url = self.path[(64 + 1):]

    expected_checksum = hashlib.sha256((secret + url).encode()).hexdigest()
    if checksum != expected_checksum:
        self.send_response(400)
        return
    url = clean_url(url) 

    # Most of these delays and commands aren't needed.
    # I have them because rare cases without delay don't work.
    command = [
        'wtype',
        '-M', 'ctrl',
        '-P', 'l',
        '-m', 'ctrl',
        '-p', 'l',
        '-s', '1000',
        '-M', 'ctrl',
        '-P', 'l',
        '-m', 'ctrl',
        '-p', 'l',
        '-s', '1000',
        url,
        '-s', '1000',
        '-k', 'KP_Enter',
        '-s', '2500',
        '-k', 'Escape',
        '-s', '1000',
        '-M', 'ctrl',
        '-P', 'r',
        '-m', 'ctrl',
        '-p', 'r',
    ]
    try:
        result = sp.run(command, check=True, text=True, capture_output=True, env=env)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(e.stdout)
        print(e.stderr)
        self.send_response(500)
        return


    self.send_response(200)
    self.send_header('Content-type', 'text/plain') 
    self.end_headers()
    self.wfile.write("ok".encode())


port = 3000
httpd = HTTPServer(('0.0.0.0', port), CastingHandler)
print("Server started on port", port)
httpd.serve_forever()