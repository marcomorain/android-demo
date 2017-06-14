#!/usr/bin/env python

from sys import argv, exit, stdout
from time import sleep
from os import system
from subprocess import check_output, CalledProcessError
from threading import Thread, Event

class StoppableThread(Thread):

  def __init__(self):
    super(StoppableThread, self).__init__()
    self._stop_event = Event()
    self.daemon = True

  def stopped(self):
    return self._stop_event.is_set()

  def run(self):
    while not self.stopped():
      stdout.write('.')
      stdout.flush()
      sleep(2)

  def stop(self):
    self._stop_event.set()

def shell_getprop(name):
    try:
        return check_output(['adb', 'shell', 'getprop', name]).strip()
    except CalledProcessError as e:
        return ''

def wait_for(name, fn):
  stdout.write('Waiting for %s' % name)
  spinner = StoppableThread()
  spinner.start()
  stdout.flush()
  while True:
    if fn():
      spinner.stop()
      print('\n%s is ready' % name)
      break
    sleep(1)


def device_ready():
    return system('adb wait-for-device') == 0

def shell_ready():
    return system('adb shell true &> /dev/null') == 0

def boot_anim_complete():
    return shell_getprop('init.svc.bootanim') == 'stopped'

usage = """
%s, a collection of tools for CI with android.

Usage:
  %s wait-for-boot - wait for a device to fully boot.
    (adb wait-for-device only waits for it to be ready for shell access).
"""

if __name__ == "__main__":

    if len(argv) != 2 or argv[1] != 'wait-for-boot':
        print(usage % (argv[0], argv[0]))
        exit(0)

    wait_for('device', device_ready)
    wait_for('shell', shell_ready)
    wait_for('boot', boot_anim_complete)





