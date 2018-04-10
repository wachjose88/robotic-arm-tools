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
The library to record sequences of movement of the arm and to play them
forward and backward.
'''

import logging
import time


class MoveCmd():

    def __init__(self, timespan, move_cmd, move_cmd_reverse):
        self.timespan = timespan
        self.move_cmd = move_cmd
        self.move_cmd_reverse = move_cmd_reverse


class Recorder():

    def __init__(self, usb_arm):
        self.usb_arm = usb_arm
        self.recording = False
        self.start_time = time.time()
        self.program = []

    def start_record(self):
        self.start_time = time.time()
        self.recording = True

    def stop_record(self):
        self.start_time = time.time()
        self.recording = False
        self.program.append(MoveCmd(0.0, [0, 0, 0], [0, 0, 0]))

    def clear_record(self):
        self.start_time = time.time()
        self.recording = False
        self.program = []

    def get_num_steps(self):
        return len(self.program)

    def get_runtime(self):
        t = 0.0
        for mc in self.program:
            t = t + mc.timespan
        return t

    def add_move_cmd(self, move_cmd, move_cmd_reverse):
        if self.recording is True:
            logging.debug('Recorder: add move')
            t = time.time() - self.start_time
            self.start_time = time.time()
            if len(self.program) > 0:
                self.program[-1].timespan = t
            self.program.append(MoveCmd(0.0, move_cmd, move_cmd_reverse))

    def play(self):
        if self.recording is False:
            for mc in self.program:
                self.usb_arm.ctrl_transfer(0x40, 6, 0x100, 0,
                                           mc.move_cmd, 1000)
                time.sleep(mc.timespan)

    def play_reverse(self):
        if self.recording is False:
            for mc in reversed(self.program):
                self.usb_arm.ctrl_transfer(0x40, 6, 0x100, 0,
                                           mc.move_cmd_reverse, 1000)
                time.sleep(mc.timespan)
            self.usb_arm.ctrl_transfer(0x40, 6, 0x100, 0,
                                       [0, 0, 0], 1000)

    def save(self, path):
        if self.recording is False:
            f = open(path, 'w')
            for mc in self.program:
                f.write('%f %d %d %d %d %d %d\n' % (mc.timespan,
                                                    mc.move_cmd[0],
                                                    mc.move_cmd[1],
                                                    mc.move_cmd[2],
                                                    mc.move_cmd_reverse[0],
                                                    mc.move_cmd_reverse[1],
                                                    mc.move_cmd_reverse[2]))
            f.close()

    def open(self, path):
        if self.recording is False:
            f = open(path, 'r')
            lines = [line.rstrip('\n') for line in f]
            f.close()
            self.program = []
            self.start_time = time.time()
            for l in lines:
                v = l.split(' ')
                move_cmd = [int(v[1]), int(v[2]), int(v[3])]
                move_cmd_reverse = [int(v[4]), int(v[5]), int(v[6])]
                self.program.append(MoveCmd(float(v[0]), move_cmd, move_cmd_reverse))
