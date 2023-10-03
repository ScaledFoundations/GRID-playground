# this script is to be run with AirGen binary built with google maps support
# before starting the binary, make sure you `settings.json` has the following entry (in the top level): "GMapsApiKey": "your_google_map_api_key"
import airgen

# Note: To use `airgen.connect_airgen(robot_type="multirotor", geo=True)`, make sure the latest airgen (>=0.0.6) is installed by (pip install airgen --upgrade)
client = airgen.connect_airgen(robot_type="multirotor", geo=True)
# otherwise, use the following two lines instead (and comment out the line above)
# client = airgen.MultirotorClient(geo=True)
# client.confirmConnection()
client.enableApiControl(True)

# Teleport vehicle to the vicinity of Seattle
geopose = airgen.GeoPose(
    airgen.GeoPoint(47.62542093668409, -122.36989783619246, 200), airgen.Quaternionr()
)
client.simSetVehicleGeoPose(geopose, True)

# Note: If you teleport the agent too far from the OriginGeoPoint mentioned in settings.json,
# it may not work properly. In that case, you should change the reference point of the world to a closer
# lat-long coordinates. You can do that either in OriginGeoPoint, or at run time through
# client.simSetGeoReference(airgen.GeoPoint(lat, long, alt))

# Takeoff
client.takeoffAsync().join()

print(client.getGpsData())

# Fly to a nearby destination
goal = airgen.GeoPoint(47.61168088062645, -122.32718628892, 200)
client.moveToGPSAsync(
    goal,
    25.0,
    timeout_sec=3e38,
    drivetrain=airgen.DrivetrainType.ForwardOnly,
    yaw_mode=airgen.YawMode(False, 0),
).join()

print(client.getGpsData())
