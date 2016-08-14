import argparse
import json
import time
from datetime import datetime
from subprocess import Popen, PIPE

from geopy.distance import vincenty

DELTA = 0.00005
METERS_PER_SEC = 1.0


class Genymotion:
    def __init__(self, shell):
        self.shell = shell

    def execute(self, command):
        process = Popen([self.shell, "-c", command], stdout=PIPE, stderr=PIPE)
        out, _ = process.communicate()
        lines = out.decode('utf-8').split("\n")
        return lines[-2]

    def set_longitude(self, longitude):
        command = "gps setlongitude " + str(longitude)
        return self.execute(command)

    def set_latitude(self, latitude):
        command = "gps setlatitude " + str(latitude)
        return self.execute(command)

    def set_location(self, now):
        print(self.set_longitude(now["lng"]))
        print(self.set_latitude(now["lat"]))

    def get_location(self):
        lat = self.execute("gps getlatitude")
        lat = lat.replace("GPS Latitude: ", "")
        lat = float(lat)
        lng = self.execute("gps getlongitude")
        lng = lng.replace("GPS Longitude: ", "")
        lng = float(lng)
        loc = {
            "lat": lat,
            "lng": lng
        }
        print(loc)
        return loc


def distance(a, b):
    a = (a["lat"], a["lng"])
    b = (b["lat"], b["lng"])
    return vincenty(a, b).meters


def run(args):
    genymotion = Genymotion(args.shell)

    with open(args.conf, "r") as f:
        conf = json.load(f)
    locations = conf["locations"]

    now = genymotion.get_location()
    genymotion.set_location(now)
    prev = {
        "lat": now["lat"],
        "lng": now["lng"],
        "time": int(datetime.now().timestamp())
    }
    while True:
        next_place = locations[0]
        dist = distance(now, next_place)

        if dist < 100:
            locations.append(locations[0])
            locations.pop(0)
            continue

        if abs(now["lat"] - next_place["lat"]) > abs(now["lng"] - next_place["lng"]):
            if now["lat"] > next_place["lat"]:
                now["lat"] -= DELTA
            else:
                now["lat"] += DELTA
        else:
            if now["lng"] > next_place["lng"]:
                now["lng"] -= DELTA
            else:
                now["lng"] += DELTA
        genymotion.set_location(now)

        # 進んだ距離
        dist = distance(now, prev)

        # 前回からの経過時間
        passed = int(datetime.now().timestamp()) - prev["time"]
        prev = {
            "lat": now["lat"],
            "lng": now["lng"],
            "time": int(datetime.now().timestamp())
        }
        # 寝なきゃいけない時間
        sleep_time = max(dist / METERS_PER_SEC - passed, 0)
        print("Sleep " + str(sleep_time) + " seconds...")
        time.sleep(sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell", required=True, help="the location of Genymotion Shell")
    parser.add_argument("--conf", required=True, help="the location of Configuration JSON file")
    run(parser.parse_args())
