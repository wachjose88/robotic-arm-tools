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
A desktop application to control the arm based on gtk.
'''

import logging
import os
from gi.repository import Gtk
from arm import RoboticArm
from recorder import Recorder


class Robot(Gtk.Window):

    def _action_base_clockwise(self, widget, data=None):
        logging.debug('Init Clockwise Base')
        self.robotic_arm.base.set_clockwise()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Clockwise Base')

    def _action_base_anticlockwise(self, widget, data=None):
        logging.debug('Init AntiClockwise Base')
        self.robotic_arm.base.set_anticlockwise()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move AntiClockwise Base')

    def _action_base_stop(self, widget, data=None):
        logging.debug('Init Stop Base')
        self.robotic_arm.base.set_stop()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Stoped Base')

    def _action_arm_up(self, widget, data=None):
        logging.debug('Init Shoulder Up')
        self.robotic_arm.shoulder.set_up()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Shoulder Up')

    def _action_arm_down(self, widget, data=None):
        logging.debug('Init Shoulder Down')
        self.robotic_arm.shoulder.set_down()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Shoulder Down')

    def _action_arm_stop(self, widget, data=None):
        logging.debug('Init Shoulder Stop')
        self.robotic_arm.shoulder.set_stop()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Stoped Shoulder')

    def _action_elbow_up(self, widget, data=None):
        logging.debug('Init Elbow Up')
        self.robotic_arm.elbow.set_up()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Elbow Up')

    def _action_elbow_down(self, widget, data=None):
        logging.debug('Init Elbow Down')
        self.robotic_arm.elbow.set_down()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Elbow Down')

    def _action_elbow_stop(self, widget, data=None):
        logging.debug('Init Elbow Stop')
        self.robotic_arm.elbow.set_stop()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Stoped Elbow')

    def _action_wrist_up(self, widget, data=None):
        logging.debug('Init Wrist Up')
        self.robotic_arm.wrist.set_up()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Wrist Up')

    def _action_wrist_down(self, widget, data=None):
        logging.debug('Init Wrist Down')
        self.robotic_arm.wrist.set_down()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Wrist Down')

    def _action_wrist_stop(self, widget, data=None):
        logging.debug('Wrist Stop')
        self.robotic_arm.wrist.set_stop()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Stoped Wrist')

    def _action_gripper_open(self, widget, data=None):
        logging.debug('Init Gripper Open')
        self.robotic_arm.gripper.set_open()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Gripper Open')

    def _action_gripper_close(self, widget, data=None):
        logging.debug('Init Gripper Close')
        self.robotic_arm.gripper.set_close()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Move Gripper Close')

    def _action_gripper_stop(self, widget, data=None):
        logging.debug('Init Gripper Stop')
        self.robotic_arm.gripper.set_stop()
        self.robotic_arm.move(self.get_run_4())
        logging.debug('Stoped Gripper')

    def _action_led(self, widget, data=None):
        if(self.led.get_label() == 'Off'):
            self.led.set_label('On')
            self.robotic_arm.light.set_on()
            self.robotic_arm.move(self.get_run_4())
            logging.debug('light: On')
            return None

        if(self.led.get_label() == 'On'):
            self.led.set_label('Off')
            self.robotic_arm.light.set_off()
            self.robotic_arm.move(self.get_run_4())
            logging.debug('light: Off')
            return None

    def _action_stop_all(self, widget, data=None):
        logging.debug('Init Stop')
        self.robotic_arm.stop()
        self.led.set_label('Off')
        logging.debug('Stoped')

    def _action_record_switch(self, widget, data=None):
        logging.debug('Init Record Switch')
        if(self.record_switch.get_label() == 'Record'):
            self.record_switch.set_label('Recording')
            self.robotic_arm.recorder.start_record()
            return None
        if(self.record_switch.get_label() == 'Recording'):
            self.record_switch.set_label('Record')
            self.robotic_arm.recorder.stop_record()
            self.nsteps_value_label.set_text(
                str(self.robotic_arm.recorder.get_num_steps()))
            m, s = divmod(int(self.robotic_arm.recorder.get_runtime()), 60)
            self.runtime_value_label.set_text(
                '%02d:%02d' % (m, s))
            return None

    def _action_record_play(self, widget, data=None):
        logging.debug('Init Record Play')
        if(self.record_switch.get_label() == 'Record'):
            self.robotic_arm.recorder.play()

    def _action_record_play_reverse(self, widget, data=None):
        logging.debug('Init Record Play Reversed')
        if(self.record_switch.get_label() == 'Record'):
            self.robotic_arm.recorder.play_reverse()

    def _action_record_clear(self, widget, data=None):
        logging.debug('Init Record Clear')
        if(self.record_switch.get_label() == 'Record'):
            self.robotic_arm.recorder.clear_record()
            self.nsteps_value_label.set_text(
                str(self.robotic_arm.recorder.get_num_steps()))
            m, s = divmod(int(self.robotic_arm.recorder.get_runtime()), 60)
            self.runtime_value_label.set_text(
                '%02d:%02d' % (m, s))

    def _action_save(self, widget, data=None):
        logging.debug('Init Save')
        dialog = Gtk.FileChooserDialog("Save recorded program",
                                       self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_path = dialog.get_filename()
            logging.debug('File selected: ' + self.file_path)
            self.file_label.set_text(os.path.basename(self.file_path))
            self.robotic_arm.recorder.save(self.file_path)
        elif response == Gtk.ResponseType.CANCEL:
            logging.debug('Cancel clicked')
        dialog.destroy()

    def _action_open(self, widget, data=None):
        logging.debug('Init Open')
        dialog = Gtk.FileChooserDialog("Please choose a recorded program",
                                       self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_path = dialog.get_filename()
            logging.debug('File selected: ' + self.file_path)
            self.file_label.set_text(os.path.basename(self.file_path))
            self.robotic_arm.recorder.open(self.file_path)
            self.nsteps_value_label.set_text(
                str(self.robotic_arm.recorder.get_num_steps()))
            m, s = divmod(int(self.robotic_arm.recorder.get_runtime()), 60)
            self.runtime_value_label.set_text(
                '%02d:%02d' % (m, s))
        elif response == Gtk.ResponseType.CANCEL:
            logging.debug('Cancel clicked')
        dialog.destroy()

    def _action_run_4_toggle(self, widget, data=None):
        logging.debug('toggle run for sec')
        self.run_4_entry.set_editable(self.run_4_toggle.get_active())

    def get_run_4(self):
        if self.run_4_toggle.get_active() is True:
            try:
                t = float(self.run_4_entry.get_value())
                if t <= 0.0:
                    return None
                return t
            except:
                return None
        else:
            return None

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        logging.debug('Init Stop')
        self.robotic_arm.stop()
        logging.debug('Stoped')
        Gtk.main_quit()

    def __init__(self):

        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            level=logging.DEBUG)
        logging.info('Start Robotic Arm Control')

        self.robotic_arm = RoboticArm()
        self.robotic_arm.recorder = Recorder(usb_arm=self.robotic_arm.usb_arm)
        self.file_path = None

        Gtk.Window.__init__(self, title='Robotic Arm Control')
        self.connect('delete_event',  self.delete_event)
        self.connect('destroy',  self.destroy)
        self.set_border_width(10)

        self.base_label = Gtk.Label('Base: ')
        self.base_label.set_alignment(0, 0)
        self.base_label.show()

        self.base_clockwise = Gtk.Button('Clockwise')
        self.base_clockwise.connect('clicked',
                                    self._action_base_clockwise, None)
        self.base_clockwise.show()

        self.base_anticlockwise = Gtk.Button('AntiClockwise')
        self.base_anticlockwise.connect('clicked',
                                        self._action_base_anticlockwise, None)
        self.base_anticlockwise.show()

        self.base_stop = Gtk.Button('Stop')
        self.base_stop.connect('clicked', self._action_base_stop, None)
        self.base_stop.show()

        self.arm_label = Gtk.Label('Shoulder: ')
        self.arm_label.set_alignment(0, 0)
        self.arm_label.show()

        self.arm_up = Gtk.Button('Up')
        self.arm_up.connect('clicked', self._action_arm_up, None)
        self.arm_up.show()

        self.arm_down = Gtk.Button('Down')
        self.arm_down.connect('clicked', self._action_arm_down, None)
        self.arm_down.show()

        self.arm_stop = Gtk.Button('Stop')
        self.arm_stop.connect('clicked', self._action_arm_stop, None)
        self.arm_stop.show()

        self.elbow_label = Gtk.Label('Elbow: ')
        self.elbow_label.set_alignment(0, 0)
        self.elbow_label.show()

        self.elbow_up = Gtk.Button('Up')
        self.elbow_up.connect('clicked', self._action_elbow_up, None)
        self.elbow_up.show()

        self.elbow_down = Gtk.Button('Down')
        self.elbow_down.connect('clicked', self._action_elbow_down, None)
        self.elbow_down.show()

        self.elbow_stop = Gtk.Button('Stop')
        self.elbow_stop.connect('clicked', self._action_elbow_stop, None)
        self.elbow_stop.show()

        self.wrist_label = Gtk.Label('Wrist: ')
        self.wrist_label.set_alignment(0, 0)
        self.wrist_label.show()

        self.wrist_up = Gtk.Button('Up')
        self.wrist_up.connect('clicked', self._action_wrist_up, None)
        self.wrist_up.show()

        self.wrist_down = Gtk.Button('Down')
        self.wrist_down.connect('clicked', self._action_wrist_down, None)
        self.wrist_down.show()

        self.wrist_stop = Gtk.Button('Stop')
        self.wrist_stop.connect('clicked', self._action_wrist_stop, None)
        self.wrist_stop.show()

        self.gripper_label = Gtk.Label('Gripper: ')
        self.gripper_label.set_alignment(0, 0)
        self.gripper_label.show()

        self.gripper_open = Gtk.Button('Open')
        self.gripper_open.connect('clicked', self._action_gripper_open, None)
        self.gripper_open.show()

        self.gripper_close = Gtk.Button('Close')
        self.gripper_close.connect('clicked', self._action_gripper_close, None)
        self.gripper_close.show()

        self.gripper_stop = Gtk.Button('Stop')
        self.gripper_stop.connect('clicked', self._action_gripper_stop, None)
        self.gripper_stop.show()

        self.led_label = Gtk.Label('Light: ')
        self.led_label.set_alignment(0, 0)
        self.led_label.show()

        self.led = Gtk.Button('Off')
        self.led.connect('clicked', self._action_led, None)
        self.led.show()

        self.stop_all = Gtk.Button('Stop All')
        self.stop_all.connect('clicked', self._action_stop_all, None)
        self.stop_all.show()

        self.image = Gtk.Image()
        self.image.set_from_file('arm.jpg')
        self.image.show()

        self.space_label = Gtk.Label(' ')
        self.space_label.set_alignment(0, 0)
        self.space_label.show()

        self.rec_label = Gtk.Label('Recorded Program:')
        self.rec_label.set_alignment(0, 0)
        self.rec_label.show()

        self.record_switch = Gtk.Button('Record')
        self.record_switch.connect('clicked', self._action_record_switch, None)
        self.record_switch.show()

        self.record_play = Gtk.Button('Play')
        self.record_play.connect('clicked', self._action_record_play, None)
        self.record_play.show()

        self.record_play_reverse = Gtk.Button('Play Reversed')
        self.record_play_reverse.connect('clicked',
                                         self._action_record_play_reverse,
                                         None)
        self.record_play_reverse.show()

        self.record_clear = Gtk.Button('Clear Program')
        self.record_clear.connect('clicked', self._action_record_clear, None)
        self.record_clear.show()

        self.file_label = Gtk.Label(' - unsaved - ')
        self.file_label.set_alignment(0, 0)
        self.file_label.show()

        self.nsteps_label = Gtk.Label('# Steps: ')
        self.nsteps_label.set_alignment(0, 0)
        self.nsteps_label.show()

        self.runtime_label = Gtk.Label('Runtime: ')
        self.runtime_label.set_alignment(0, 0)
        self.runtime_label.show()

        self.nsteps_value_label = Gtk.Label('0')
        self.nsteps_value_label.set_alignment(0, 0)
        self.nsteps_value_label.show()

        self.runtime_value_label = Gtk.Label('00:00')
        self.runtime_value_label.set_alignment(0, 0)
        self.runtime_value_label.show()

        self.save = Gtk.Button('Save')
        self.save.connect('clicked', self._action_save, None)
        self.save.show()

        self.open = Gtk.Button('Open')
        self.open.connect('clicked', self._action_open, None)
        self.open.show()

        adj = Gtk.Adjustment(2.0, 0.0, 100.0, 0.1)
        self.run_4_entry = Gtk.SpinButton()
        self.run_4_entry.configure(adj, 0.1, 2)
        self.run_4_entry.show()

        self.run_4_toggle = Gtk.CheckButton('Run for sec:')
        self.run_4_toggle.set_active(False)
        self.run_4_toggle.connect('toggled', self._action_run_4_toggle, None)
        self.run_4_toggle.show()

        self.controls = Gtk.Grid()
        self.controls.attach(self.base_label, 0, 0, 1, 1)
        self.controls.attach(self.base_clockwise, 1, 0, 1, 1)
        self.controls.attach(self.base_stop, 2, 0, 1, 1)
        self.controls.attach(self.base_anticlockwise, 3, 0, 1, 1)
        self.controls.attach(self.arm_label, 0, 1, 1, 1)
        self.controls.attach(self.arm_up, 1, 1, 1, 1)
        self.controls.attach(self.arm_stop, 2, 1, 1, 1)
        self.controls.attach(self.arm_down, 3, 1, 1, 1)
        self.controls.attach(self.elbow_label, 0, 2, 1, 1)
        self.controls.attach(self.elbow_up, 1, 2, 1, 1)
        self.controls.attach(self.elbow_stop, 2, 2, 1, 1)
        self.controls.attach(self.elbow_down, 3, 2, 1, 1)
        self.controls.attach(self.wrist_label, 0, 3, 1, 1)
        self.controls.attach(self.wrist_up, 1, 3, 1, 1)
        self.controls.attach(self.wrist_stop, 2, 3, 1, 1)
        self.controls.attach(self.wrist_down, 3, 3, 1, 1)
        self.controls.attach(self.gripper_label, 0, 4, 1, 1)
        self.controls.attach(self.gripper_open, 1, 4, 1, 1)
        self.controls.attach(self.gripper_stop, 2, 4, 1, 1)
        self.controls.attach(self.gripper_close, 3, 4, 1, 1)
        self.controls.attach(self.led_label, 0, 5, 1, 1)
        self.controls.attach(self.led, 1, 5, 3, 1)
        self.controls.attach(self.stop_all, 1, 6, 3, 1)
        self.controls.attach(self.image, 4, 0, 1, 7)
        self.controls.attach(self.run_4_toggle, 0, 7, 2, 1)
        self.controls.attach(self.run_4_entry, 2, 7, 2, 1)
        self.controls.attach(self.space_label, 0, 8, 5, 1)
        self.controls.attach(self.rec_label, 0, 9, 5, 1)
        self.controls.attach(self.file_label, 0, 10, 5, 1)
        self.controls.attach(self.record_switch, 4, 10, 1, 1)
        self.controls.attach(self.record_play, 4, 11, 1, 1)
        self.controls.attach(self.record_play_reverse, 4, 12, 1, 1)
        self.controls.attach(self.record_clear, 4, 13, 1, 1)
        self.controls.attach(self.nsteps_label, 0, 12, 2, 1)
        self.controls.attach(self.runtime_label, 0, 13, 2, 1)
        self.controls.attach(self.nsteps_value_label, 2, 12, 2, 1)
        self.controls.attach(self.runtime_value_label, 2, 13, 2, 1)
        self.controls.attach(self.save, 0, 14, 4, 1)
        self.controls.attach(self.open, 4, 14, 1, 1)
        self.controls.show()

        self.add(self.controls)
        self.show()
        logging.info('Started Robotic Arm Control')

    def main(self):
        Gtk.main()

if __name__ == '__main__':
    robot = Robot()
    robot.main()
