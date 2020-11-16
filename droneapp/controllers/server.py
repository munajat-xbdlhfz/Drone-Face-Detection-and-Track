import logging

from flask import jsonify
from flask import render_template
from flask import request
from flask import Response

from droneapp.models.drone_manager import DroneManager

import config


logger = logging.getLogger(__name__)
app = config.app


def get_drone():
    return DroneManager()


@app.route('/')
def index():
    return render_template('controller.html')


@app.route('/api/command/', methods=['POST'])
def command():
    cmd = request.form.get('command')
    logger.info({'action': 'command', 'cmd': cmd})
    drone = get_drone()
    # Drone Takeoff
    if cmd == 'takeoff':
        drone.takeoff()
    # Drone Land
    if cmd == 'land':
        drone.land()

    # Drone Go Up
    if cmd == 'up':
        drone.up()
    # Drone Go Down
    if cmd == 'down':
        drone.down()
    # Drone Go Left
    if cmd == 'left':
        drone.left()
    # Drone Go Right
    if cmd == 'right':
        drone.right()

    #Drone Move Forward
    if cmd == 'forward':
        drone.forward()
    # Drone Move Backward
    if cmd == 'back':
        drone.back()
    # Drone Turn Right
    if cmd == 'clockwise':
        drone.clockwise()
    # Drone Turn left
    if cmd == 'counterClockwise':
        drone.counter_clockwise()
    
    # Drone Doing Flip
    if cmd == 'flipFront':
        drone.flip_front()
    if cmd == 'flipBack':
        drone.flip_back()
    if cmd == 'flipLeft':
        drone.flip_left()
    if cmd == 'flipRight':
        drone.flip_right()
    
    # Drone Command For Face Detect and Tracking the Face
    if cmd == 'faceDetectAndTrack':
        drone.enable_face_detect()
    if cmd == 'stopFaceDetectAndTrack':
        drone.disable_face_detect()

    # Command For taking Snapshot From Drone
    if cmd == 'snapshot':
        if drone.snapshot():
            return jsonify(status='success'), 200
        else:
            return jsonify(status='fail'), 400

    return jsonify(status='success'), 200

# Generate Video From Drone into Image
def video_generator():
    drone = get_drone()
    for jpeg in drone.video_jpeg_generator():
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                jpeg +
                b'\r\n\r\n')

@app.route('/video/streaming')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')


def run():
    app.run(host=config.WEB_ADDRESS,
            port=config.WEB_PORT,
            threaded=True)