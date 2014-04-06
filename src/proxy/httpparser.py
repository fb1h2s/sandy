#!/usr/bin/env python
import socket

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser
from http_parser.util import b

def main():

    p = HttpParser()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    body = []
    header_done = False
    try:
        s.connect(('install2.optimum-installer.com', 80))
        s.send(b("GET /o/PDFCreator/Express_Installer.exe.exe HTTP/1.1\r\nHost: gunicorn.org\r\n\r\n"))

        while True:
            data = s.recv(1024)
            if not data:
                break

            recved = len(data)
            nparsed = p.execute(data, recved)
            assert nparsed == recved

            if p.is_headers_complete() and not header_done:
                print(p.get_headers())
                print(p.get_headers()['content-length'])
                header_done = True

            if p.is_partial_body():
                body.append(p.recv_body())
                print p.recv_body()
                print "BDy++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

            if p.is_message_complete():
                break

        body = b("").join(body)
        
        print "Writing file\n"
        data_write = open("mal.exe","wb") 
        data_write.write(body)
        data_write.close()
        
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    finally:
        s.close()

if __name__ == "__main__":
    main()


