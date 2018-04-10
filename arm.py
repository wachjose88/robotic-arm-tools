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
The library to control the arm.
'''

import usb.core
import usb.util
import time


class Component():

    def __init__(self):
        self.state = 0
        self.factor = 1

    def set_stop(self):
        self.state = 0

    def set_up(self):
        self.state = 1

    def set_down(self):
        self.state = 2

    def compute_move(self):
        return self.state * self.factor

    def compute_move_reverse(self):
        s = self.state
        if s == 1:
            s = 2
        elif s == 2:
            s = 1
        return s * self.factor

    def get_state_text(self):
        s = ''
        if self.state == 1:
            s = 'Up'
        elif self.state == 2:
            s = 'Down'
        elif self.state == 0:
            s = 'Stopped'
        return s


class Base(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 1

    def set_clockwise(self):
        self.state = 1

    def set_anticlockwise(self):
        self.state = 2

    def get_state_text(self):
        s = ''
        if self.state == 1:
            s = 'Clockwise'
        elif self.state == 2:
            s = 'AntiClockwise'
        elif self.state == 0:
            s = 'Stopped'
        return s


class Shoulder(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 64


class Elbow(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 16


class Wrist(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 4


class Gripper(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 1

    def set_close(self):
        self.state = 1

    def set_open(self):
        self.state = 2

    def get_state_text(self):
        s = ''
        if self.state == 1:
            s = 'Close'
        elif self.state == 2:
            s = 'Open'
        elif self.state == 0:
            s = 'Stopped'
        return s


class Light(Component):

    def __init__(self):
        Component.__init__(self)
        self.factor = 1

    def set_on(self):
        self.state = 1

    def set_off(self):
        self.state = 0

    def get_state_text(self):
        s = ''
        if self.state == 1:
            s = 'On'
        elif self.state == 0:
            s = 'Off'
        return s


class RoboticArm():

    def __init__(self, usb_vendor=0x1267, usb_product=0x0000, recorder=None):
        self.usb_arm = usb.core.find(idVendor=usb_vendor,
                                     idProduct=usb_product)
        if self.usb_arm is None:
            raise ValueError("'Arm not found")

        self.base = Base()
        self.shoulder = Shoulder()
        self.elbow = Elbow()
        self.wrist = Wrist()
        self.gripper = Gripper()
        self.light = Light()

        self.recorder = recorder

        self.last_move = [0, 0, 0]

    def move_changed(self, current_move):
        if (current_move[0] == self.last_move[0]
            and current_move[1] == self.last_move[1]
            and current_move[2] == self.last_move[2]):
            return False
        return True

    def move(self, run_4_time=None):
        a = 0
        b = 0
        l = 0
        a = a + self.shoulder.compute_move()
        a = a + self.elbow.compute_move()
        a = a + self.wrist.compute_move()
        a = a + self.gripper.compute_move()
        b = b + self.base.compute_move()
        l = l + self.light.compute_move()
        cmd = [a, b, l]
        if self.move_changed(cmd) is True:
            self.usb_arm.ctrl_transfer(0x40, 6, 0x100, 0, cmd, 1000)
            self.last_move = cmd

            if self.recorder is not None:
                a = 0
                b = 0
                l = 0
                a = a + self.shoulder.compute_move_reverse()
                a = a + self.elbow.compute_move_reverse()
                a = a + self.wrist.compute_move_reverse()
                a = a + self.gripper.compute_move_reverse()
                b = b + self.base.compute_move_reverse()
                l = l + self.light.compute_move()
                self.recorder.add_move_cmd(cmd, [a, b, l])

            if run_4_time is not None:
                time.sleep(run_4_time)
                self.base.set_stop()
                self.shoulder.set_stop()
                self.elbow.set_stop()
                self.wrist.set_stop()
                self.gripper.set_stop()
                self.light.set_off()
                self.usb_arm.ctrl_transfer(0x40, 6, 0x100, 0, [0, 0, 0], 1000)
                self.last_move = [0, 0, 0]

                if self.recorder is not None:
                    self.recorder.add_move_cmd([0, 0, 0], [0, 0, 0])

    def stop(self):
        self.base.set_stop()
        self.shoulder.set_stop()
        self.elbow.set_stop()
        self.wrist.set_stop()
        self.gripper.set_stop()
        self.light.set_off()
        self.move()
