import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3',config=Config(signature_version='s3v4'))

sms_bucket = s3.Bucket('sms.masterpartner.cloud')
build_bucket = s3.Bucket('smsbuild.masterpartner.cloud')

sms_zip = StringIO.StringIO()
build_bucket.download_fileobj('smsbuild.zip',sms_zip)

with zipfile.ZipFile(sms_zip) as myzip:
  for nm in myzip.namelist():
      obj = myzip.open(nm)
      sms_bucket.upload_fileobj(obj,nm,
        ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
      sms_bucket.Object(nm).Acl().put(ACL='public-read')
