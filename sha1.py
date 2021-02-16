#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

def secure_hash_algorithm_1(file):
    with open(file, 'rb')as f:
        data = f.read()
    sha1 = hashlib.sha1()
    sha1.update(data)
    return sha1.hexdigest()

def main():
    print(secure_hash_algorithm_1(input()))

if __name__ == '__main__':
    main()
