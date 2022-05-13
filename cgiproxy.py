#!/usr/bin/env python3

import os
import sys
import urllib
import http.client
import urllib.parse
import urllib.request

TARGET = "http://127.0.0.1/~ondra/test"
TARGET = "//127.0.0.1/~ondra/test"

def main():
    method = os.environ.get("REQUEST_METHOD") or "GET"
    content_type = os.environ.get("CONTENT_TYPE")
    content_length = os.environ.get("CONTENT_LENGTH")
    query_string = os.environ.get("QUERY_STRING")
    query_string = os.environ.get("PATH_INFO")

    o = urllib.parse.urlparse(TARGET)

    scheme = o.scheme or 'http'
    if scheme not in ("http", "https"):
        raise ValueError("only http and https targets are supported")
    hostname = o.hostname
    port = o.port

    if scheme == 'http':
        port = port or 80
        conn = http.client.HTTPConnection(host, port)
    elif scheme == 'https':
        port = port or 443
        conn = http.client.HTTPSConnection(host, port)

    conn.request(method, "/")
    resp = conn.getresponse()

    sys.stdout.buffer.write(
        b"%s %s %s\r\n" % (resp.version, resp.status, resp.reason))
    for header, value in resp.headers:
        if header.lower() in ("transfer-encoding", "content-length"):
            continue
        sys.stdout.buffer.write("{}: {}\r\n".format(header, value).encode('latin-1'))

    sys.stdout.buffer.write(b'\r\n')
    body = resp.read()
    sys.stdout.buffer.write(body)

    print(hostname, port)


if __name__ == "__main__":
    try:
        fwdgwr
        main()
    except Exception as e:
        sys.stdout.buffer.write(b'HTTP/1.1 500 proxy internal error\r\n')
        sys.stdout.buffer.write(b'\r\n\r\n')
        sys.stdout.buffer.write(str(e).encode('utf-8'))


