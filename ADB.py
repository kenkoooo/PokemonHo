import random
import string
import subprocess
import time
from subprocess import Popen, PIPE


class AndroidDeviceBridge:
    def __init__(self, path):
        self.path = path
        self.width, self.height = self.get_solution()
        self.png = "/tmp/" \
                   + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)]) \
                   + ".png"

    def get_solution(self):
        process = Popen([self.path, "shell", "wm", "size"], stdout=PIPE, stderr=PIPE)
        out, _ = process.communicate()
        lines = out.decode('utf-8').split()
        width, height = lines[-1].split("x")
        return int(width), int(height)

    def adb_exec(self, commands):
        commands = [str(c) for c in commands]
        commands.insert(0, self.path)
        commands.insert(1, "shell")
        commands.insert(2, "input")
        subprocess.check_output(commands)
        time.sleep(1)

    def swipe(self, x1, y1, x2, y2):
        duration = 200
        self.adb_exec(["swipe", x1, y1, x2, y2, duration])

    def tap(self, x, y):
        self.adb_exec(["touchscreen", "tap", x, y])

    def swipe_poke_stop(self):
        x1 = int(self.width * 0.2)
        x2 = int(self.width * 0.8)
        y = int(self.height * 0.4)
        self.swipe(x1, y, x2, y)
        self.tap_cancel()

    def tap_cancel(self):
        x = int(self.width / 2)
        y = int(self.height * 5 / 6)
        self.tap(x, y)

    def send_to_doctor(self):
        x = int(self.width * 15 / 16)
        y = int(self.height * 5 / 6)
        self.tap(x, y)
        y = int(self.height * 3 / 4)
        self.tap(x, y)
        x = int(self.width / 2)
        y = int(self.height * 7 / 12)
        self.tap(x, y)
        time.sleep(1)

    def capture_screen(self):
        command = self.path + " shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > " + self.png
        subprocess.check_output(command, shell=True)

    def throw_ball(self):
        height = random.uniform(0.05, 0.55)
        y1 = int(self.height * 0.7)
        y2 = int(self.height * height)
        x = int(self.width / 2)
        self.swipe(x, y1, x, y2)

    def random_tap(self):
        x = random.uniform(0.25, 0.75)
        x = int(self.width * x)
        y = random.uniform(0.5, 0.625)
        y = int(self.height * y)
        self.tap(x, y)
