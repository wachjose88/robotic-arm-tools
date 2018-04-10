# MIT License
#
# Copyright (c) 2015-2018 Josef Wachtler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
A web application to control the arm based on flask.
'''

from flask import Flask, jsonify, render_template, request, Response
import argparse
from camera import CameraStream
from arm import RoboticArm


robotic_arm = RoboticArm()
camera_number = 0
app = Flask(__name__, static_folder='web/static',
            template_folder='web/templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control')
def control():
    return render_template('control.html')


@app.route('/base')
def base():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.base.set_clockwise()
        robotic_arm.move()
    elif status == 2:
        robotic_arm.base.set_anticlockwise()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.base.set_stop()
        robotic_arm.move()
    return jsonify(result=robotic_arm.base.state,
                   result_text=robotic_arm.base.get_state_text())


@app.route('/shoulder')
def shoulder():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.shoulder.set_up()
        robotic_arm.move()
    elif status == 2:
        robotic_arm.shoulder.set_down()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.shoulder.set_stop()
        robotic_arm.move()
    return jsonify(result=robotic_arm.shoulder.state,
                   result_text=robotic_arm.shoulder.get_state_text())


@app.route('/elbow')
def elbow():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.elbow.set_up()
        robotic_arm.move()
    elif status == 2:
        robotic_arm.elbow.set_down()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.elbow.set_stop()
        robotic_arm.move()
    return jsonify(result=robotic_arm.elbow.state,
                   result_text=robotic_arm.elbow.get_state_text())


@app.route('/wrist')
def wrist():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.wrist.set_up()
        robotic_arm.move()
    elif status == 2:
        robotic_arm.wrist.set_down()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.wrist.set_stop()
        robotic_arm.move()
    return jsonify(result=robotic_arm.wrist.state,
                   result_text=robotic_arm.wrist.get_state_text())


@app.route('/gripper')
def gripper():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.gripper.set_close()
        robotic_arm.move()
    elif status == 2:
        robotic_arm.gripper.set_open()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.gripper.set_stop()
        robotic_arm.move()
    return jsonify(result=robotic_arm.gripper.state,
                   result_text=robotic_arm.gripper.get_state_text())


@app.route('/light')
def light():
    status = request.args.get('status', 0, type=int)
    if status == 1:
        robotic_arm.light.set_on()
        robotic_arm.move()
    elif status == 0:
        robotic_arm.light.set_off()
        robotic_arm.move()
    return jsonify(result=robotic_arm.light.state,
                   result_text=robotic_arm.light.get_state_text())


@app.route('/stop')
def stop():
    robotic_arm.stop()
    return jsonify(result=0,
                   result_text='Stopped')


@app.route('/cam')
def cam():
    return render_template('cam.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(CameraStream(camera_number)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A web controller for the Robotic Arm Kit.')
    parser.add_argument('-c', '--camera',
                        help='The system number of the camera.', required=False)
    args = parser.parse_args()
    if args.camera is not None:
        camera_number = int(args.camera)
    app.run(debug=True, threaded=True)
