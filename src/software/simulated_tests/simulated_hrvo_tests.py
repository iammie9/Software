import pytest
 
import software.python_bindings as tbots
from software.simulated_tests.robot_enters_region import *
from software.simulated_tests.ball_enters_region import *
from software.simulated_tests.ball_moves_forward import *
from software.simulated_tests.friendly_has_ball_possession import *
from software.simulated_tests.ball_speed_threshold import *
from software.simulated_tests.robot_speed_threshold import *
from software.simulated_tests.excessive_dribbling import *
from software.simulated_tests.simulated_test_fixture import (
   simulated_test_runner,
   pytest_main,
)
from proto.message_translation.tbots_protobuf import create_world_state
from proto.ssl_gc_common_pb2 import Team
 
# The x value of the wall in front of the friendly robot
front_wall_x = -2
# each gate refers to the center to center distance between each wall and the front
# wall The constant offsets can be tweaked to get different distances between each wall
gate_1 = 1
gate_2 = gate_1 + 2
gate_3 = gate_2 + 1
robot_y_delta = 0.2
# margin around destination point
threshold = 0.05
 
@pytest.mark.parametrize(
   "ball_initial_position,ball_initial_velocity,robot_initial_position, robot_destination",
   [
       # test drive in straight line with moving enemy robot from behind
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(-2.3,0)], [tbots.Point(2.8,0)]),
       # test drive in straight line with moving enemy robot from side
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(-2.5,0)], [tbots.Point(2.8,0)]),
       # test drive in straight line with no obstacle
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(-2.5,0)], [tbots.Point(2.8,0)]),
       # test drive in straight line with friendly robot infront  
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(-2.5,0)], [tbots.Point(2.8,0)]),
       # test single enemy directly infront
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(0.7,0)], [tbots.Point(2,0)]),
       # test three robot wall
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(0,0)], [tbots.Point(2.8,0)]),
       # test zig zag movement
       (
           tbots.Point(0,-2),
           tbots.Vector(0,0),
           [tbots.Point(front_wall_x - 0.5, 0)],
           [tbots.Point(front_wall_x + gate_3 + 0.5, 0)]
       ),
       # test agent not going in static obstacles
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(2.9,-1)], [tbots.Point(2.9,1)]),
       # test start in local minima
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(0.7,0)], [tbots.Point(2.8,0)]),
       # test start in local minima with open end
       (tbots.Point(1,2), tbots.Vector(0,0), [tbots.Point(-2.5,0)], [tbots.Point(2.8,0)]),
       # TODO test robot avoiding ball obstacle
   ],
)
