import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node, PushRosNamespace
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration as LC

config_dir = os.path.join(
    get_package_share_directory('mercury_mapping'),
    'config'
)


def generate_launch_description():
    # declare the launch args to read for this file
    DeclareLaunchArgument(
        "robot",
        default_value="mercury",
        description="Namespace of the vehicle",
    ),

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            "robot",
            default_value="mercury",
            description="name of the robot"
        ),

        DeclareLaunchArgument(
            "config",
            default_value="config",
            description="name of maps to use"
        ),

        DeclareLaunchArgument(
            "config_yaml",
            default_value=[LC('config'), ".yaml"]
        ),

        GroupAction([
            PushRosNamespace(
                LC("robot")
            ),

            # create the nodes
            Node(
                package='mercury_mapping',
                executable='mapping.py',
                name='mercury_mapping',
                respawn=True,
                output='screen',

                # use the parameters on the node
                parameters=[
                    PathJoinSubstitution([
                        config_dir,
                        LC("config_yaml")
                    ])
                ]
            ),

            Node(
                package="chameleon_tf",
                executable="chameleon_tf",
                name="world_to_map",
                output="screen",
                respawn=True,
                parameters=[
                    {"stddev_threshold": 0.5},
                    {"source_frame": "world"},
                    {"target_frame": "map"},
                    {"initial_translation": [
                        0.0,
                        0.0,
                        0.0
                    ]},
                    {"initial_rotation": [
                        0.0,
                        0.0,
                        0.0
                    ]},
                    {"transform_locks": [
                        False,      # unlock x
                        False,      # unlock y
                        True,       # lock z
                        True,       # lock roll
                        True,       # lock pitch
                        False       # unlock yaw
                    ]}
                ]
            )
        ], scoped=True)
    ])
