#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Carlos da Costa (https://github.com/cdacos), refer to LICENSE.txt

from boto.s3.connection import S3Connection
import sys, decrypt_lib

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
key.get_contents_to_filename(save_to)

encryption_info_str = key.get_metadata('cb-encryptioninfo')
# <version>;<sourcesize>;<algo>;<keysize_in_bits>;<Base64encodedIV>;;<Compression>;
encryption_info = encryption_info_str.split(';')
base64iv = encryption_info[4]

decrypt_lib.decrypt(password, base64iv, save_to)

