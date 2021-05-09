#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            print("装饰器")
            return func(*args, **kwargs)
        except Exception as e:
            print(type(e))
            print(e)
    return wrapper

@handle_error
def foo():
    with open("Python.txt", encoding="utf-8")as f:
        for i in f:
            print(i.strip())
    print(0 + "A")

def main():
    foo()

if __name__ == '__main__':
    main()
