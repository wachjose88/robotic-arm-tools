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
Control the arm using a wii-mote.
'''

import cwiid
import time
from arm import RoboticArm


class WiiMote():

    def __init__(self):
        self.wm = None
        self.wm_roll_start = 0
        self.wm_pitch_start = 0
        self.robotic_arm = RoboticArm()
        print('Robotic Arm controlled by Wiimote!')


    def print_help(self):
        row = '| {:<20} | {:<20} |'
        texts = [
            ('Base clockwise', 'roll wiimote right'),
            ('Base anti clockwise', 'roll wiimote left'),
            ('Shoulder up', 'wiimote nose up'),
            ('Shoulder down', 'wiimote nose down'),
            ('Ellbow up', 'press button "UP"'),
            ('Ellbow down', 'press button "DOWN"'),
            ('Wrist up', 'press button "A"'),
            ('Wrist down', 'press button "B"'),
            ('open Gripper', 'press button "LEFT"'),
            ('close Gripper', 'press button "RIGHT"'),
            ('Light on', 'press button "PLUS"'),
            ('Light off', 'press button "MINUS"'),
            ('Stop all and exit', 'press button "HOME"'),
        ]
        print(' ')
        print('Ready to go!')
        print(' ')
        print('-' * 47)
        print(row.format('Robotic Arm moves', 'Wiimote Command'))
        print('-' * 47)
        for t in texts:
            print(row.format(*t))
        print('-' * 47)


    def connect(self):
        print(' ')
        i=2
        print('Connect to wiimote (hold 1 + 2) ...')
        while not self.wm:
            try:
                self.wm=cwiid.Wiimote()
            except RuntimeError:
                if (i>10):
                    quit()
                    break
                print('Error opening wiimote connection')
                print('attempt ' + str(i))
                i +=1
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

        self.wm.led = 1
        print('Connected!')


    def calibrate(self):
        print(' ')
        print('Hold the wiimote in your neutral possition and press A to calibrate')
        while True:
            if (self.wm.state['buttons'] & cwiid.BTN_A):
                self.wm_roll_start = self.wm.state['acc'][0]
                self.wm_pitch_start = self.wm.state['acc'][1]
                break

            time.sleep(0.01)

        self.wm.led = 3
        print self.wm_roll_start
        print self.wm_pitch_start
        print('Calibrated!')


    def run(self):
        self.print_help()
        while True:
            if (self.wm.state['buttons'] & cwiid.BTN_HOME):
                self.robotic_arm.stop()
                break

            lt = self.wm_roll_start - 10
            rt = self.wm_roll_start + 10
            if (self.wm.state['acc'][0] < lt):
                self.robotic_arm.base.set_anticlockwise()
            elif (self.wm.state['acc'][0] > rt):
                self.robotic_arm.base.set_clockwise()
            else:
                self.robotic_arm.base.set_stop()

            ut = self.wm_pitch_start - 10
            dt = self.wm_pitch_start + 10
            if (self.wm.state['acc'][1] < ut):
                self.robotic_arm.shoulder.set_up()
            elif (self.wm.state['acc'][1] > dt):
                self.robotic_arm.shoulder.set_down()
            else:
                self.robotic_arm.shoulder.set_stop()

            if (self.wm.state['buttons'] & cwiid.BTN_UP):
                self.robotic_arm.elbow.set_up()
            elif (self.wm.state['buttons'] & cwiid.BTN_DOWN):
                self.robotic_arm.elbow.set_down()
            else:
                self.robotic_arm.elbow.set_stop()

            if (self.wm.state['buttons'] & cwiid.BTN_A):
                self.robotic_arm.wrist.set_up()
            elif (self.wm.state['buttons'] & cwiid.BTN_B):
                self.robotic_arm.wrist.set_down()
            else:
                self.robotic_arm.wrist.set_stop()

            if (self.wm.state['buttons'] & cwiid.BTN_LEFT):
                self.robotic_arm.gripper.set_open()
            elif (self.wm.state['buttons'] & cwiid.BTN_RIGHT):
                self.robotic_arm.gripper.set_close()
            else:
                self.robotic_arm.gripper.set_stop()

            if (self.wm.state['buttons'] & cwiid.BTN_PLUS):
                self.robotic_arm.light.set_on()
            elif (self.wm.state['buttons'] & cwiid.BTN_MINUS):
                self.robotic_arm.light.set_off()

            #print self.wm.state['acc']
            self.robotic_arm.move()
            time.sleep(0.01)


if __name__ == '__main__':
    wiim = WiiMote()
    wiim.connect()
    wiim.calibrate()
    wiim.run()
