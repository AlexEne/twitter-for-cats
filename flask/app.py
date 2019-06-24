import json
import boto3
from flask import Flask, render_template, request, Response
import botocore
import datetime

app = Flask(__name__)

dynamodb = boto3.resource(
    'dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
table = dynamodb.Table('Mews')


# dynamodb.create_table(
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'Name',
#             'AttributeType': 'S',
#         },
#         {
#             'AttributeName': 'Mew',
#             'AttributeType': 'S',
#         },
#     ],
#     KeySchema=[
#         {
#             'AttributeName': 'Name',
#             'KeyType': 'HASH',
#         },
#         {
#             'AttributeName': 'Mew',
#             'KeyType': 'RANGE',
#         },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5,
#     },
#     TableName="Mews",
# )


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/about')
def about():
    return 'Here is the about page!'


@app.route('/mews')
def mews():
    mews = table.scan()["Items"]
    return json.dumps(mews)


def is_valid_mew(name, mew):
    return name != '' and mew != ''


@app.route('/postmew', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        request_json = request.get_json()
        print(request.get_json())
        name = request_json.get('name')
        mew = request_json.get('content')
        if is_valid_mew(name, mew):
            response = table.put_item(
                Item={
                    'Name': name,
                    'Mew': mew,
                    'Date': str(datetime.datetime.now())
                }
            )
            print("PutItem succeeded:")
            print(json.dumps(response, indent=4))

            response = table.scan()
            print(response)
            for i in response["Items"]:
                print(i)

            return Response('', status=200, mimetype='application/json')
        else:
            error = {"error": "please provide a valid mew!"}
            return Response(json.dumps(error),
                            status=422, mimetype='application/json')
    else:
        mews = table.scan()["Items"]
        return Response(json.dumps(mews),
                        status=422, mimetype='application/json')
    return "Do a post request!"


if __name__ == '__main__':
    app.run(debug=True)
