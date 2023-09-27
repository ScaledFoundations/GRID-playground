# this script is to be run with AirGen binary built with google maps support
# before starting the binary, make sure you `settings.json` has the following entry (in the top level): "GMapsApiKey": "your_google_map_api_key"
import airgen

client = airgen.MultirotorClient(geo=True)
client.confirmConnection()
client.enableApiControl(True)

# Teleport vehicle to Palo Alto airport
geopose = airgen.GeoPose(
    airgen.GeoPoint(37.460605351257186, -122.11457389426046, 0), airgen.Quaternionr()
)
client.simSetVehicleGeoPose(geopose, True)

# Takeoff
client.takeoffAsync().join()

print(client.getGpsData())

# Fly to Moffett Field
goal = airgen.GeoPoint(37.41299434959267, -122.05396149400366, 50)
client.moveToGPSAsync(
    goal,
    25.0,
    timeout_sec=3e38,
    drivetrain=airgen.DrivetrainType.ForwardOnly,
    yaw_mode=airgen.YawMode(False, 0),
).join()

print(client.getGpsData())
