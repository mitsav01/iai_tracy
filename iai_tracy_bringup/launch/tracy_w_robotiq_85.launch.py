from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():


    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")
    # General arguments
    kinematics_params_file = LaunchConfiguration("kinematics_params_file")
    joint_limit_params_file = LaunchConfiguration("joint_limit_params_file")
    description_file = LaunchConfiguration("description_file")
    tf_prefix = LaunchConfiguration("tf_prefix")
    reverse_ip = LaunchConfiguration("reverse_ip")
    script_command_port = LaunchConfiguration("script_command_port")
    reverse_port = LaunchConfiguration("reverse_port")
    script_sender_port = LaunchConfiguration("script_sender_port")
    trajectory_port = LaunchConfiguration("trajectory_port")

    # Left arm
    left_arm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                FindPackageShare('ur_robot_driver').find('ur_robot_driver'),
                'launch',
                'ur10e_bringup.launch.py'
            )
        ),
        launch_arguments={
            'robot_ip': '192.168.102.154',
            'tf_prefix': 'left_',
            'controller_config_file': os.path.join(
                FindPackageShare('iai_tracy_ur').find('iai_tracy_ur'),
                'config',
                'ur10e_controllers_left.yaml'
            ),
            'controllers': 'joint_state_controller_left scaled_pos_joint_traj_controller_left',
            'stopped_controllers': 'pos_joint_traj_controller_left',
            'kinematics_config': LaunchConfiguration('kinematics_config_left'),
            'robot_description_file': os.path.join(
                FindPackageShare('iai_tracy_description').find('iai_tracy_description'),
                'launch',
                'upload.launch.py'
            ),
            'reverse_port': '50011',
            'script_sender_port': '50012',
            'trajectory_port': '50013',
            'script_command_port': '50014'
        }.items()
    )

    # Right arm
    right_arm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                FindPackageShare('ur_robot_driver').find('ur_robot_driver'),
                'launch',
                'ur10e_bringup.launch.py'
            )
        ),
        launch_arguments={
            'robot_ip': '192.168.102.153',
            'tf_prefix': 'right_',
            'controller_config_file': os.path.join(
                FindPackageShare('iai_tracy_ur').find('iai_tracy_ur'),
                'config',
                'ur10e_controllers_right.yaml'
            ),
            'controllers': 'joint_state_controller_right scaled_pos_joint_traj_controller_right',
            'stopped_controllers': 'pos_joint_traj_controller_right',
            'kinematics_config': LaunchConfiguration('kinematics_config_right'),
            'robot_description_file': os.path.join(
                FindPackageShare('iai_tracy_description').find('iai_tracy_description'),
                'launch',
                'upload.launch.py'
            ),
            'reverse_port': '50001',
            'script_sender_port': '50002',
            'trajectory_port': '5003',
            'script_command_port': '50005'
        }.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument('kinematics_config_left'),
        DeclareLaunchArgument('kinematics_config_right'),
        left_arm_launch,
        right_arm_launch
    ])