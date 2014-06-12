#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Carlos da Costa (https://github.com/cdacos)
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from boto.s3.connection import S3Connection
import base64, os, sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Based on information provided by:
# http://www.cloudberrylab.com/forum/yaf_postsm10753_Decrypt-files-in-computer-without-Cloudberry.aspx#post10753

unpad = lambda s : s[0:-ord(s[-1])]

if len(sys.argv) < 6 or sys.argv[1] == '-h':
  print 'Usages:'
  print '1. Specify everything:'
  print '... aws_access_key aws_secret_key bucket_name password bucket_key save_to'
  print '2. Save to local directory using name of the downloaded file:'
  print '... aws_access_key aws_secret_key bucket_name password bucket_key'
  exit()

aws_access_key =  sys.argv[1]
aws_secret_key =  sys.argv[2]
bucket_name    =  sys.argv[3]
password       =  sys.argv[4] # Cloudberry client-side encryption password
path           =  sys.argv[5] # Full path in bucket (not including bucket name itself)
save_to        =  sys.argv[6] if len(sys.argv) == 7 else ''  # If ends in a / specifies directory

conn = S3Connection(aws_access_key, aws_secret_key)
bucket = conn.get_bucket(bucket_name)
key = bucket.get_key(path)

if not key:
  print 'Key not found, aborting.'
  exit()

if not save_to or save_to.endswith('/'):
  save_to = save_to + key.name.split('/')[-1]
key.get_contents_to_filename(save_to + '.tmp')

encryption_info_str = key.get_metadata('cb-encryptioninfo')
# <version>;<sourcesize>;<algo>;<keysize_in_bits>;<Base64encodedIV>;;<Compression>;
encryption_info = encryption_info_str.split(';')
base64iv = encryption_info[4]
iv = base64.b64decode(base64iv)

key_size = 32 #AES256
iterations = 1000

derived_key = PBKDF2(password, bytearray(8).decode('utf-8'), key_size, iterations)

encrypted_file = open(save_to + '.tmp', 'rb')
data = encrypted_file.read()
encrypted_file.close()

cipher = AES.new(derived_key, AES.MODE_CBC, iv)
decrypted = unpad(cipher.decrypt(data))

decrypted_file = open(save_to, 'wb')
decrypted_file.write(decrypted)
decrypted_file.close()

os.remove(save_to + '.tmp')
