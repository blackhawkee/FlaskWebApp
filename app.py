import requests
from flask import Flask, render_template, Response, jsonify, json
from camera import VideoCamera
import cv2

app = Flask(__name__)

video_stream = VideoCamera()

@app.route('/')
def index():
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

@app.route('/onClick', methods=['GET', 'POST','DELETE', 'PATCH'])
def onClick():
    encoding = 'utf-8'
    imageByteStr = str(video_stream.get_frame_string())
    imageByteStr = 'data:image/jpeg;base64,' + imageByteStr[2:-1]
    # print(str('--frame\r\n Content-Type: image/jpeg\r\n\r\nb' + (video_stream.get_frame().decode(encoding)) + '\r\n\r\n'))

    URL = 'http://faceidentify-http-ace-dashboard-prod.mycluster-220882-a0206187d3c93bf725a210436d6057c3-0000.us-south.containers.appdomain.cloud:80/image/v1/postImage'
    myobj = {'imageData': imageByteStr}
    output = requests.post(url = URL, data = json.dumps(myobj))

    testResponse = output.json()
    outputObj = {'OutputPersonName': testResponse["PersonName"]}
    # print(outputObj)
    response = jsonify(outputObj)
    # response.status_code = 200  # or 400 or whatever
    # return testResponse["PersonName"]
    print(response)
    return response

    # return str(str(video_stream.get_frame_string()))
    # return ("nothing")

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")




















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
