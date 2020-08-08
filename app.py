# import os
# from http.server import HTTPServer, CGIHTTPRequestHandler

import requests
from flask import Flask, render_template, Response, jsonify, json, request
# from camera import VideoCamera
# import cv2
# from cloudant.client import Cloudant
# from cloudant.error import CloudantException
# from cloudant.result import Result, ResultByKey

# from upload import uploadGDrive
# from webserver import webServer

app = Flask(__name__)

# video_stream = VideoCamera()


@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('1-basics.html')


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(video_stream),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/onClick', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def onClick():
    print(str(request.get_data()))
    imageByteStr = str(request.get_data())
    imageByteStr = imageByteStr[2:-1]
    # return 'Response from Python onClick function'
    # encoding = 'utf-8'
    # imageByteStr = str(video_stream.get_frame_string())
    # imageByteStr = 'data:image/jpeg;base64,' + imageByteStr[2:-1]
    # # print(str('--frame\r\n Content-Type: image/jpeg\r\n\r\nb' + (video_stream.get_frame().decode(encoding)) + '\r\n\r\n'))
    # # imagePath = str(video_stream.get_frame_file())
    #
    # # URL = 'http://faceidentify-http-ace-dashboard-prod.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud:80/image/v1/postImage'
    URL = 'https://api.my-apic-01.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud/face-recognition-app/faceidentity/image/v1/postImage';
    headers = {'X-IBM-Client-Id': '4f024aa09a2a1e353aa1eb80c628f289'}
    myobj = {'imageData': imageByteStr}
    # print(myobj)
    # myobj = {'imageUrl': imagePath}
    print('Request to FaceRecog API ==== ' + str(myobj))
    output = requests.post(url=URL, data=json.dumps(myobj), headers=headers, verify=False)
    print('Text Format Response from FaceRecog API ==== ' + output.text)
    testResponse = output.json()
    print('JSON Format Response from FaceRecog API ==== ' + str(testResponse))

    cloudantresponse = _getdetailsfromcloudantapi(testResponse)
    print('Response from Cloudant API ==== ' + str(cloudantresponse.json()))
    return cloudantresponse.json()


def _getdetailsfromcloudantapi(getpersonaldetailsinput):
    cloudanturl = 'https://api.my-apic-01.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud/face-recognition-app/faceidentity/getPerson/';
    # cloudantheaders = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-IBM-Client-Id': '4f024aa09a2a1e353aa1eb80c628f289'}
    cloudantheaders = {'X-IBM-Client-Id': '4f024aa09a2a1e353aa1eb80c628f289', 'Content-Type': 'application/json',
                       'Accept': 'application/json'}
    myobj = {'className': getpersonaldetailsinput["PersonName"]}
    # myobj = {'className': 'Niranjan'}
    myobjjson = json.dumps(myobj)
    # print(myobjjson)
    response = requests.post(url=cloudanturl, data=myobjjson, headers=cloudantheaders, verify=False)
    return response

if __name__ == '__main__':
    # app.run(host='127.0.0.1', debug=True, port="5000")
    app.run(host='0.0.0.0', debug=True, port="5000")

