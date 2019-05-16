from urllib.request import urlopen
import json
import zipfile
import boto3
import io
import time
import mimetypes

def getFileFromGit():
    return urlopen("https://github.com/leobeosab/RyanWise.Me/archive/master.zip").read()

def invalidateAllCFFiles():
    distID = "E8G7ATUPBJEIE"

    cloudFrontConn = boto3.client('cloudfront')
    cloudFrontConn.create_invalidation(
        DistributionId=distID, 
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']
            },
            'CallerReference': 'Lambda:'+ str(time.time())
        })

def uploadZipToS3():
    s3Target = 'ryanwise.me' #bucket name
    buildFolder = '/_site/' #build subdir

    s3 = boto3.client('s3')
    
    putObjects = []
    with io.BytesIO(getFileFromGit()) as tf:
        tf.seek(0)
        with zipfile.ZipFile(tf, mode='r') as zipf:
            for file in zipf.infolist():
                filePath = file.filename
                filePath = filePath.split(buildFolder)
                if len(filePath) != 2 or len(filePath[1]) == 0 or filePath[1].endswith('/'): 
                    #We only want the _site/* files with no path before it
                    continue

                fileName = filePath[1]

                #Guess the mime type
                mimetype, _ = mimetypes.guess_type(fileName)
                if mimetype is None:
                    mimetype = 'binary/octet-stream'

                putFile = s3.put_object(Bucket=s3Target, Key=fileName, Body=zipf.read(file), ACL='public-read', ContentType=mimetype)

                putObjects.append(putFile)
                print(fileName)

    if len(putObjects) > 0:
        invalidateAllCFFiles()
        return "Success!"
    else:
        return "Error"

def handle(event, context):

    body = ""
    statusCode = 200

    try:
       body = uploadZipToS3() 
    except Exception as e:
        statusCode = 500
        body = "\n" + str(e)

    return {
        'statusCode': statusCode,
        'body': json.dumps(body)
    }

uploadZipToS3()