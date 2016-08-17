from subprocess import Popen, PIPE


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
