#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Carlos da Costa (https://github.com/cdacos), refer to LICENSE.txt

import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

unpad = lambda s : s[0:-ord(s[-1])]

def decrypt(password, base64iv, file_to_decrypt):
  iv = base64.b64decode(base64iv)

  key_size = 32 #AES256
  iterations = 1000

  derived_key = PBKDF2(password, bytearray(8).decode('utf-8'), key_size, iterations)

  encrypted_file = open(file_to_decrypt, 'rb')
  data = encrypted_file.read()
  encrypted_file.close()

  cipher = AES.new(derived_key, AES.MODE_CBC, iv)
  decrypted = unpad(cipher.decrypt(data))

  decrypted_file = open(file_to_decrypt, 'wb')
  decrypted_file.write(decrypted)
  decrypted_file.close()

