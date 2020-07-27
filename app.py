import os
from http.server import HTTPServer, CGIHTTPRequestHandler

import requests
from flask import Flask, render_template, Response, jsonify, json, request
from camera import VideoCamera
import cv2
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_script import Manager, Server


from upload import uploadGDrive
from webserver import webServer

app = Flask(__name__)

video_stream = VideoCamera()
# upload_gdrive = uploadGDrive()
# web_server = webServer()

@app.route('/')
def index():
    # webServer()
    return render_template('index.html')



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
        return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/onClick', methods=['GET', 'POST','DELETE', 'PATCH'])
# def onClick():
#     encoding = 'utf-8'
#     # bytesStream = video_stream.get_frame
#     # print(str(video_stream.get_frame_file()))
#     upload_gdrive.uploadBytesToGDrive(video_stream.get_frame_file())
#
#     tempDict = {'name':'name', 'accountId':'accountId', 'accountType':'accountType', 'balance':'balance', 'mainBranch':'mainBranch'}
#     response = jsonify(tempDict)
#     return response


@app.route('/onClick', methods=['GET', 'POST','DELETE', 'PATCH'])
def onClick():
    encoding = 'utf-8'
    # imageByteStr = str(video_stream.get_frame_string())
    # imageByteStr = 'data:image/jpeg;base64,' + imageByteStr[2:-1]
    # print(str('--frame\r\n Content-Type: image/jpeg\r\n\r\nb' + (video_stream.get_frame().decode(encoding)) + '\r\n\r\n'))
    imagePath = str(video_stream.get_frame_file())

    URL = 'http://faceidentify-http-ace-dashboard-prod.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud:80/image/v1/postImage'
    # myobj = {'imageData': imageByteStr}
    myobj = {'imageUrl': imagePath}
    output = requests.post(url = URL, data = json.dumps(myobj))

    testResponse = output.json()

    getDetailsInpObj = {'personname': testResponse["PersonName"]}
    # getDetailsInpObj = {'personname': 'Niranjan'}
    getDetailsInpObj = jsonify(getDetailsInpObj)
    # print(getDetailsInpObj)
    getDetailsOutObj = _getDetailsFromCloudant(getDetailsInpObj)
    # print(str(getDetailsOutObj))
    tempstr = str(getDetailsOutObj)
    tempstr = tempstr[1:-1]
    tempstr = tempstr.replace("':", "\":")
    tempstr = tempstr.replace("', '", "', \"")
    tempstr = tempstr.replace("{'", "{\"")
    tempstr = tempstr.replace("\":", "\" :")
    tempstr = tempstr.replace("'", "\"")
    print(tempstr)
    tempDict = json.loads(tempstr)
    # tempstr.replace("'", "\"")
    # print(json.dumps(tempDict))
    # print('START----->' + tempstr[1:-1] + '<------END')


    # outputObj = {'OutputPersonName': testResponse["PersonName"]}
    # print(outputObj)
    # response = jsonify(outputObj)
    response = jsonify(tempDict)
    # response.status_code = 200  # or 400 or whatever
    # return testResponse["PersonName"]
    # print(response)
    return response

    # return str(str(video_stream.get_frame_string()))
    # return ("nothing")

@app.route('/getDetails', methods=['GET', 'POST','DELETE', 'PATCH'])
def _getDetailsFromCloudant(person):
    client = Cloudant("a3197aee-3b78-4540-8417-c536bd4da1b7-bluemix",
                      "7fb911920babd92e5184cc7139b2760c6ac1c04f44384627de50f3db8d3d441a",
                      url="https://a3197aee-3b78-4540-8417-c536bd4da1b7-bluemix:7fb911920babd92e5184cc7139b2760c6ac1c04f44384627de50f3db8d3d441a@a3197aee-3b78-4540-8417-c536bd4da1b7-bluemix.cloudant.com")

    client.connect()
    database_name = "facerecog"
    my_database = client.create_database(database_name)

    # inputData = request.get_json()
    # print('input' + str(person.get_json().get('personname')))
    # print('input' + str(inputData.get('personname')))

    if my_database.exists():
        # print(f"'{database_name}' database exists.")
        # my_document = my_database['ee7492a6cb4f98dead06240c6f156207']
        # my_document = my_database['Niranjan']
        # selector = {'name': {'$eq': 'Niranjan'}}
        # selector = {'name': {'$eq': str(inputData.get('personname'))}}
        selector = {'name': {'$eq': str(person.get_json().get('personname'))}}
        docs = my_database.get_query_result(selector)
        dbobj = docs.all()
        # print(docs.all())
        # print(dbobj)
        return dbobj
        # result_collection = Result(my_database.all_docs, include_docs=True)
        #
        # for result in result_collection:
        #     print(result['doc'])
        #     # if result['name']=='Niranjan':
        #     #     outresponse = result
        #     #     return jsonify(outresponse)




# def custom_call():
#     # Make sure the server is created at current directory
#     app.run(host='127.0.0.1', debug=True, port="5000")
#     print('starting web server')
#     os.chdir('./temp/')
#     # Create server object listening the port 80
#     server_object = HTTPServer(server_address=('127.0.0.1', 8001), RequestHandlerClass=CGIHTTPRequestHandler)
#     # Start the web server
#     server_object.serve_forever()
#     pass
#
# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         custom_call()
#         #Hint: Here you could manipulate app
#         return Server.__call__(self, app, *args, **kwargs)
#
# app = Flask(__name__)
# manager = Manager(app)
#
# # Remeber to add the command to your Manager instance
# manager.add_command('runserver', CustomServer())
#
# if __name__ == "__main__":
#     manager.run()

# with app.app_context():
#     webServer()
#
# def run():
#     app.run(debug=True, use_reloader=False)
#     # app.run(host='127.0.0.1', debug=True, port="5000")

if __name__ == '__main__':
    # webServer()
    app.run(host='127.0.0.1', debug=True, port="5000")
    # app.run()
    # print('after run of flask')
    # webServer()
    # print('after starting the webserver')





















# from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, json
# import cv2
# import requests
#
# app = Flask(__name__)
#
#
# @app.route('/index.html')
# def backuphome():
#     return render_template('Layout.html')
#
# # #Capture video from webcam
# # vid_capture = cv2.VideoCapture(0)
# # vid_cod = cv2.VideoWriter_fourcc(*'XVID')
# # output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, 20.0, (640,480))
# # while(True):
# #      # Capture each frame of webcam video
# #      ret,frame = vid_capture.read()
# #      cv2.imshow("My cam video", frame)
# #      output.write(frame)
# #      # Close and break the loop after pressing "x" key
# #      if cv2.waitKey(1) &0XFF == ord('x'):
# #          break
# # # close the already opened camera
# # vid_capture.release()
# # # close the already opened file
# # output.release()
# # # close the window and de-allocate any associated memory usage
#
# @app.route('/backup/pythonImagePost', methods=['GET', 'POST','DELETE', 'PATCH'])
# def backuppostImage():
#     URL = 'http://faceidentify-http-ace-dashboard-prod.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud:80/image/v1/postImage'
#     inputData = request.get_json()
#     myobj = {'imageData': str(inputData.get('base64data'))}
#     output = requests.post(url = URL, data = json.dumps(myobj))
#
#     testResponse = output.json()
#     outputObj = {'OutputPersonName': testResponse["PersonName"]}
#     response = jsonify(outputObj)
#     response.status_code = 200  # or 400 or whatever
#     return response
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8983)
