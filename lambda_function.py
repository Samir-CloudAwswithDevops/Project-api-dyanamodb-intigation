import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    if method == "GET":
        with open("index.html", "r") as f:
            html = f.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }

    elif method == "POST":
        body = urllib.parse.parse_qs(event.get("body", ""))
        fname = body.get("fname", [""])[0]
        email = body.get("email", [""])[0]

        # Save to DynamoDB
        table = boto3.resource("dynamodb").Table("dibya")
        table.put_item(Item={"username": fname, "email": email})

        with open("success.html", "r") as f:
            html = f.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }

    else:
        return {"statusCode": 405, "body": "Method Not Allowed"}
