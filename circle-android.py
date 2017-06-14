#!/usr/bin/env python

from sys import argv, exit, stdout
from time import sleep
from os import system
from subprocess import check_output, CalledProcessError
from threading import Thread

class Spinner:
    busy = False
    delay = 2

    def __init__(self, delay=None):
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            stdout.write('.')
            stdout.flush()
            sleep(self.delay)

    def start(self):
        self.busy = True
        thread = Thread(target=self.spinner_task)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.busy = False
        sleep(self.delay)


def shell_getprop(name):
    try:
        return check_output(['adb', 'shell', 'getprop', name]).strip()
    except CalledProcessError as e:
        return ''

"""
adb_shell_getprop () {
    adb shell getprop $1 | tr -d [:space:] # delete the whitespace
}
device_actually_ready () {
    # https://devmaze.wordpress.com/2011/12/12/starting-and-stopping-android-emulators/
    [ "$(adb_shell_getprop init.svc.bootanim)" = "stopped" ]
}
if [ "$1" == "wait-for-boot" ]
then
    # wait for the device to respond to shell commands
    spin_until adb shell true 2> /dev/null
    echo adb shell connected.
    # wait for the emulator to be completely finished booting.
    # adb wait-for-device is not sufficient for this.
    spin_until device_actually_ready
    echo Boot animation complete.
else
i

"""

def wait_for(name, fn):
  stdout.write('Waiting for %s' % name)
  spinner = Spinner()
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





