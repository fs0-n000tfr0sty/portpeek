#!/usr/bin/env python3
"""portpeek: tiny tcp connect checker. only point it at machines you own."""
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

COMMON = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379, 8080]


def check(host, port, timeout=0.5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)  # 0.5s is plenty on a lan
        return port if s.connect_ex((host, port)) == 0 else None


def main():
    if len(sys.argv) < 2:
        print("usage: portpeek.py <host> [port,port,...]")
        return 1
    host = sys.argv[1]
    ports = [int(p) for p in sys.argv[2].split(",")] if len(sys.argv) > 2 else COMMON
    with ThreadPoolExecutor(max_workers=32) as pool:
        for port in pool.map(lambda p: check(host, p), ports):
            if port:
                print(f"{port}/tcp open")
    return 0


if __name__ == "__main__":
    sys.exit(main())
