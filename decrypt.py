#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Carlos da Costa (https://github.com/cdacos), refer to LICENSE.txt

import sys, decrypt_lib

if len(sys.argv) < 3 or sys.argv[1] == '-h':
  print 'Usage:'
  print '... password base64-iv file'
  print 'For the base64-iv you need to find the value of the cb-encryptioninfo header. It will have a semi-colon seperated string like: 1;190728;AES;256;kgAAAAAAwlXSWZGeLJlaWg==;;;'
  print 'The 5th item is the base64 encoded "IV" value which is kgAAAAAAwlXSWZGeLJlaWg== in this case. You will need this to decrypt the file (it is different for each file).'
  exit()

password     =  sys.argv[1] # Cloudberry client-side encryption password
base64iv     =  sys.argv[2] # Base64 IV from 'cb-encryptioninfo' metadata header
decrypt_file =  sys.argv[3]

decrypt_lib.decrypt(password, base64iv, decrypt_file)
