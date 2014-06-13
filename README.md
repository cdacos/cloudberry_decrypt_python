# Cloudberry Decrypt for Python

Created to decrypt files encrypted by Cloudberry Bare Metal Backup and uploaded to Amazon S3.

Requires:
 - boto (http://aws.amazon.com/sdkforpython/)
 - pycrypto (https://www.dlitz.net/software/pycrypto/)

## Installation
Recommend working in a virtualenv.

1. Clone the repo:
```
git clone git@github.com:cdacos/cloudberry_decrypt_python.git```

2. To create the virtualenv:
```
virtualenv cloudberry_decrypt```

3. To start the virtualenv:
```
cd cloudberry_decrypt
source bin/activate```

4. Install the AWS Python tools :
```
pip install boto
pip install pycrypto```

5. Now run the scripts as shown below. For example:
```
python s3_download.py -h``` 

6. To close the virtualenv:
```
deactivate```


## Example Usage

### Pull from Amazon S3 and decrypt in one step
Use ```s3_download.py```. You will need your AWS S3 access and secret keys. The name of the bucket, and then the bucket_key (the path to the specific file, beginning with a / and not including the bucket name). The password is the one you entered into the Cloudberry backup tool to encrypt the data before uploading to Amazon S3. The optional ```save_to``` argument can be the path to a specific file, or a directory if it ends with a /. If not specified the file name is taken from the bucket key.
```
python s3_download.py aws_access_key aws_secret_key bucket_name password bucket_key [save_to]```

#### Example:
```
python s3_download.py "YOUR-AWS-ACCESS-KEY" "Your-AWS-Secret-Key" "mybackupbucket" "My-very-awesome-and-long-encryption-password" "/CBB_MYMACHINE/D:/Projects/SampleSite/WebRoot/web.config:/20131205160904/web.config"
```
Will result in web.config being downloaded, decrypted and saved in the working directory.

### Decrypt a file already downloaded
If you've already downloaded the file and want to decrypt it, use ```decrypt.py```. 

```
python decrypt.py password base64-iv file
```

But first you will need to use an S3 client (or the Amazon S3 website) to look at the metadata for the file. You need to find the value of the **cb-encryptioninfo** header. It will have a semi-colon seperated string like:
```
1;190728;AES;256;kgAAAAAAwlXSWZGeLJlaWg==;;;```
The 5th item is the base64 encoded "IV" value which is ```kgAAAAAAwlXSWZGeLJlaWg==``` in this case. You will need this to decrypt the file (it is different for each file):
```
python decrypt.py "My-very-awesome-and-long-encryption-password" "kgAAAAAAwlXSWZGeLJlaWg==" "An Example.pdf"
```

## TODO
* Decrypt large files
* Support compression

## Creator

Carlos da Costa

* http://twitter.com/cdacos
* https://github.com/cdacos

## Copyright and license
Refer LICENSE.txt
