from commonroad.visualization.draw_dispatch_cr import draw_object
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.scenario.obstacle import DynamicObstacle, ObstacleType, ObstacleRole, Occupancy
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from commonroad.geometry.shape import Circle
from commonroad.scenario.trajectory import State, Trajectory


def load_scenarion_file(scenario):
    scenario_dir = os.path.join(os.path.dirname(os.getcwd()), 'scenarios')
    return os.path.join(scenario_dir, scenario)


def add_simple_object(scenario, id, position_x, position_y, oritentation, velocity, *args, **kwargs):
    init_state = State(position=np.array(
        [position_x, position_y]), orientation=oritentation, velocity=velocity)
    new_obstacle = DynamicObstacle(
        id, ObstacleType.PEDESTRIAN, Circle(10.0), init_state)
    scenario.add_objects(new_obstacle)


def add_simple_object_or_fail(*args, **kwargs):
    try:
        add_simple_object(*args, **kwargs)
        return True
    except Exception as e:
        print('{}'.format(e))
        return False


def get_object_state(scenario, object_id):
    obj = scenario.obstacle_by_id(object_id)
    if obj:
        return obj.initial_state
    return None


def format_insert_for_communication(result):
    return "INSERT_OK" if result else "ERROR"


def format_state_for_communication(state):
    if state is None:
        return ''
    else:
        return '{} {} {} {}'.format(
            state.position[0],
            state.position[1],
            state.orientation,
            state.velocity
        )


def setup_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', metavar='ID',
                        type=int, help='ID of the new object')
    parser.add_argument('position_x', metavar='X',
                        type=float, help='Position X of the new object')
    parser.add_argument('position_y', metavar='Y',
                        type=float, help='Position Y of the new object')
    parser.add_argument('orientation', metavar='Ψ',
                        type=float, help='Orientation Ψ of the new object')
    parser.add_argument('velocity', metavar='v',
                        type=float, help='Velicty v of the new object')
    parser.add_argument(
        '--get-state', metavar='ID', type=int, help='Specify the ID of an Object to get the state back')
    return parser


def main():
    args = setup_arg_parser()
    parsed_args = args.parse_args()
    scenario_file_name = 'C-USA_Lanker-1_1_T-1.xml'
    file_path = load_scenarion_file(scenario_file_name)
    scenario, planning_problem_set = CommonRoadFileReader(file_path).open()
    result = add_simple_object_or_fail(scenario, *(vars(parsed_args).values()))
    out = format_insert_for_communication(result)
    if (parsed_args.get_state):
        state = get_object_state(scenario, parsed_args.get_state)  # 11434
        out += " " + format_state_for_communication(state)
    print(out)


if __name__ == '__main__':
    main()
