#!/usr/bin/env python3

import os
import sys
import urllib
import posixpath
import http.client
import urllib.parse
import urllib.request

TARGET = "http://127.0.0.1/~ondra/test"
TARGET = "//127.0.0.1/~ondra/"

def main():
    method = os.environ.get("REQUEST_METHOD") or "GET"
    content_type = os.environ.get("CONTENT_TYPE")
    content_length = os.environ.get("CONTENT_LENGTH")
    query_string = os.environ.get("QUERY_STRING")
    path_info = os.environ.get("PATH_INFO") or '/'

    o = urllib.parse.urlparse(TARGET)

    scheme = o.scheme or 'http'
    if scheme not in ("http", "https"):
        raise ValueError("only http and https targets are supported")
    host = o.hostname
    port = o.port
    path = o.path

    if scheme == 'http':
        port = port or 80
        conn = http.client.HTTPConnection(host, port)
    elif scheme == 'https':
        port = port or 443
        conn = http.client.HTTPSConnection(host, port)

    target_path = posixpath.join(path, path_info.lstrip('/'))
    q = target_path + (('?' + query_string) if query_string else '')

    has_body = method.upper() in ("PUT", "POST", "PATCH")

    headers = dict()
    if not has_body:
        conn.request(method, q, headers=headers)
    else:
        if content_length:
            content_length = int(content_length)
            body = sys.stdin.buffer.read(int(content_length))
            if len(body) != content_length:
                sys.stderr.write(
                    "Content-Length is {}, got {}\r\n"
                    .format(len(body), content_length))
        else:
            body = sys.stdin.buffer.read()
        headers["Content-Length"] = str(len(body)).encode('latin-1')
        if content_type:
            headers["Content-Type"] = content_type
        conn.request(method, q, body=body, headers=headers)

    resp = conn.getresponse()

    outbuf = b""
    outbuf += (b"Status: %d %s\r\n"
            % (resp.status, resp.reason.encode("latin-1"))) 

    for header in resp.headers:
        if header.lower() in ("transfer-encoding", "content-length"):
            continue
        outbuf += header.encode('latin-1')
        outbuf += b": "
        outbuf += resp.headers[header].encode('latin-1')
        outbuf += b'\r\n'

    body = resp.read()
    outbuf += b"Content-Length: %d\r\n" % (len(body),)

    outbuf += b'\r\n'  # end of headers
    outbuf += f"path_info {path_info}\r\n".encode('latin-1')
    outbuf += f"query_string {query_string}\r\n".encode('latin-1')
    outbuf += f"path {o.path}\r\n".encode('latin-1')
    outbuf += f"content_length {content_length}\r\n".encode('latin-1')
    outbuf += f"content_type {content_type}\r\n".encode('latin-1')
    outbuf += f"target_path {target_path}\r\n".encode('latin-1')
    outbuf += body

    sys.stdout.buffer.write(outbuf)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        verbose = True
        import traceback
        sys.stdout.buffer.write(b'status: 500 proxy internal error\r\n')
        sys.stdout.buffer.write(b'content-type: text/html\r\n')
        sys.stdout.buffer.write(b'\r\n')
        if verbose:
            sys.stdout.buffer.write(traceback.format_exc().encode('utf-8'))
        else:
            sys.stdout.buffer.write(str(e).encode('utf-8'))
        sys.stdout.buffer.write(b'\r\n')


