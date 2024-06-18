#!/usr/bin/python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import hashlib
import subprocess as sp
import os

env = os.environ.copy()
env["WAYLAND_DISPLAY"] = "wayland-1"

with open('/etc/machine-id', 'r') as file:
    machine_id = file.read().strip()
token = hashlib.sha256(machine_id.encode()).hexdigest()
print("Token for checksum:", token)

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

    expected_checksum = hashlib.sha256((token + url).encode()).hexdigest()
    if checksum != expected_checksum:
        self.send_response(400)
        return
    url = clean_url(url) 

    command = [
        'wtype',
        '-M', 'ctrl',
        '-P', 'l',
        '-m', 'ctrl',
        '-p', 'l',
        '-s', '100',
        url,
        '-k', 'KP_Enter',
        '-s', '2000',
        '-k', 'Escape'
    ]
    sp.run(command, check=True, text=True, env=env)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain') 
    self.end_headers()
    self.wfile.write("ok".encode())


port = 3000
httpd = HTTPServer(('0.0.0.0', port), CastingHandler)
print("Server started on port", port)
httpd.serve_forever()