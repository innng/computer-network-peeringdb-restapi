#!/usr/bin/env python3

import socket
from sys import argv


def main():
    ipPort = argv[1].split(':')
    host = ipPort[0]
    port = int(ipPort[1])
    opt = int(argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == '__main__':
    main()
