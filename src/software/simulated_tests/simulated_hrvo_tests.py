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

def simulated_hrvo_tests(
   ball_initial_position,
   ball_initial_velocity,
   robot_initial_position,
   robot_destination_position
   simulated_test_runner,
):
   # Setup Robot
   simulated_test_runner.simulator_proto_unix_io.send_proto(
       WorldState,
       create_world_state(
           yellow_robot_locations=[], # currently no enemy robot positions
           blue_robot_locations=[robot_initial_position], # tbots positions
           ball_location=ball_initial_position,
           ball_velocity=ball_initial_velocity,
       ),
   )
 
   # These aren't necessary for this test, but this is just an example
   # of how to send commands to the simulator.
   #
   # NOTE: The gamecontroller responses are automatically handled by
   # the gamecontroller context manager class
   simulated_test_runner.gamecontroller.send_ci_input(
       gc_command=Command.Type.STOP, team=Team.UNKNOWN
   )
   simulated_test_runner.gamecontroller.send_ci_input(
       gc_command=Command.Type.FORCE_START, team=Team.BLUE
   )
 
   # TODO set up tactics
    params = AssignedTacticPlayControlParams()
    params.assigned_tactics[0].move.CopyFrom(
        MoveTactic(
            destination=robot_destination,
            final_orientation=robot_desired_orientation,
            final_speed=0.0,
            dribbler_mode=DribblerMode.OFF,
            ball_collision_type=BallCollisionType.ALLOW,
            auto_chip_or_kick=AutoChipOrKick(autokick_speed_m_per_s=0.0),
            max_allowed_speed_mode=MaxAllowedSpeedMode.PHYSICAL_LIMIT,
            target_spin_rev_per_s=0.0,
        )
    )
    simulated_test_runner.blue_full_system_proto_unix_io.send_proto(
        AssignedTacticPlayControlParams, params
    )

    # Setup no tactics on the enemy side
    params = AssignedTacticPlayControlParams()
    simulated_test_runner.yellow_full_system_proto_unix_io.send_proto(
        AssignedTacticPlayControlParams, params
    )
 
   # Always Validation
   always_validation_sequence_set = [
   ]
 
   # Eventually Validation
   # TODO add robotStationaryInPolygon(1, expected_final_position, 15, world_ptr, yield) to eventually_validation
   eventually_validation_sequence_set = [
       [
           # Small circle around the destination point that the robot should be stationary within for 15 ticks
           # Circle(robot_destination, threshold)
           circle_bound = tbots.Circle(robot_destination, threshold)
           RobotEventuallyEntersRegion(
               regions=[circle_bound]
           ),
       ]
   ]
 
   simulated_test_runner.run_test(
       eventually_validation_sequence_set=eventually_validation_sequence_set,
       always_validation_sequence_set=always_validation_sequence_set,
   )
   
 
if __name__ == "__main__":
   pytest_main(__file__)

