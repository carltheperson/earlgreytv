from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import hashlib
import uuid
import subprocess as sp
import base64

# Token based on MAC address
mac = ''.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
token = hashlib.sha256(mac.encode()).hexdigest()[0:18]
print("Token client should know", token)

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
    parsed_path = urlparse(self.path)
    query_params = parse_qs(parsed_path.query)
    url = query_params["url"][0]
    token_ = query_params["t"][0]
    if token_ != token:
       self.send_response(400)
       return
    url = clean_url(url) 

    url_b64 = base64.b64encode(url.encode()).decode('utf-8')
    command = f'wtype -M ctrl -P l -m ctrl -p l -s 100 "$(echo \'{url_b64}\' | base64 -d)" -k KP_Enter -s 2000 -k Escape'
    result = sp.run(command, shell=True, check=True, text=True)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain') 
    self.end_headers()
    self.wfile.write("ok".encode())


port = 3000
httpd = HTTPServer(('0.0.0.0', port), CastingHandler)
print("Server started on port", port)
httpd.serve_forever()