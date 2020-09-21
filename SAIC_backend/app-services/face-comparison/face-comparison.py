import boto3
import json
import os
from itertools import combinations

bucket_name = os.environ["BUCKETNAME"]
s3 = boto3.resource("s3")
client=boto3.client('rekognition')

def lambda_handler(event, context):
    if type(event) == str:
        event = json.loads(event)
    event["headers"] = json.loads(json.dumps(event["headers"]).lower())    
    outputdata = {}
    try:
        resultdata = []
        image_list = []
        # creatig bucket object to read the images
        my_bucket = s3.Bucket(bucket_name)
        for my_bucket_object in my_bucket.objects.all():
            image_list.append(my_bucket_object.key)
        # generating image combination
        image_comb = combinations(image_list, 2) 
        #loop through combination to compare images
        for i in list(image_comb): 
            comparision_data = {}
            sourceFilename = list(i)[0]
            targetFilename = list(i)[1]
            response=client.compare_faces(SimilarityThreshold=0,SourceImage={'S3Object':{'Bucket':bucket_name,'Name':sourceFilename}},TargetImage={'S3Object':{'Bucket':bucket_name,'Name':targetFilename}})
            comparision_data["SourceImage"] = sourceFilename
            comparision_data["TargetImage"] = targetFilename
            comparision_data["Similarity"] = response["FaceMatches"][0]["Similarity"]
            comparision_data["Confidence"] = response["FaceMatches"][0]["Face"]["Confidence"]
            resultdata.append(comparision_data)
        outputdata["status"] = "Success"
        outputdata["message"] = "Success"
        outputdata["output"] = resultdata          
    except Exception as e:
        outputdata["status"] = "Failure"
        outputdata["message"] = str(e)
        outputdata["output"] = []
    print(outputdata)
    if outputdata["status"] == "Success":
        return {"statusCode": 200,"headers": {"Access-Control-Allow-Headers": "Content-Type","Access-Control-Allow-Origin": "*","Access-Control-Allow-Methods": "GET,POST,PUT,DELETE"},"body": json.dumps(outputdata)}
    else:
        return {"statusCode": 403,"headers": {"Access-Control-Allow-Headers": "Content-Type","Access-Control-Allow-Origin": "*","Access-Control-Allow-Methods": "GET,POST,PUT,DELETE"},"body": json.dumps(outputdata)}

if __name__ == "__main__": 
    event = {"headers":{}, "queryStringParameters":None}
    lambda_handler(event, None)    