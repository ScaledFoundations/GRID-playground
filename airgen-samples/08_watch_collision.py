# collision
# collision points are designed for Block environment

from typing import Tuple, List
import time
import airgen

# import a function decorator that monitors collision
# see documentation for more details and usage
from airgen.utils.collect import collision_collector


client = airgen.connect_airgen(robot_type="multirotor")
client.enableApiControl(True)
client.takeoffAsync().join()


@collision_collector()
def move(client, x, y, z, **kwargs) -> None | Tuple[None, list]:
    future = client.moveToPositionAsync(x, y, z, 3)
    future.start_waiting()
    while future.is_completed is None:
        # waiting it to complete
        time.sleep(1)


@collision_collector()
def move2(client, x, y, z, **kwargs) -> None | Tuple[None, list]:
    # or just use below one-liner, which is equivalent to the above move
    client.moveToPositionAsync(x, y, z, 3).join()


# todo: fix the linter error
_, collisions = move(
    client, 0, 0, -10, _stop_at_collision=True, _collect_collision=True
)  # noqa
print(collisions)

_, collisions = move(
    client,
    20,
    20,
    -10,
    _stop_at_collision=True,
    _collect_collision=True,
)
print(collisions)

# Note
#   if no explict action is applied to drone after collision (like `__stop_at_collision__`, which puts drone in hover state),
#   The behavior of drone is not clearly defined, it will try to recover from collision, but it also start drifting to a random direction.
