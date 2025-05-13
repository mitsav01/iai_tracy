import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node


def generate_launch_description():
    # Package paths
    desc_pkg = get_package_share_directory('iai_tracy_description')
    ur_pkg = get_package_share_directory('iai_tracy_ur')
    urdf_file = os.path.join(desc_pkg, 'urdf', 'tracy.urdf.xacro')

    # Kinematics file paths
    l_kinematics_file = os.path.join(ur_pkg, 'include', 'iai_tracy_ur', 'left_ur10e_calibration.yaml')
    r_kinematics_file = os.path.join(ur_pkg, 'include', 'iai_tracy_ur', 'right_ur10e_calibration.yaml')

    # Declare arguments
    declared_args = [
        DeclareLaunchArgument('urdf', default_value=urdf_file),
        DeclareLaunchArgument('transmission_hw_interface', default_value='hardware_interface/PositionJointInterface'),
        DeclareLaunchArgument('kinematics_config_left', default_value=l_kinematics_file),
        DeclareLaunchArgument('kinematics_config_right', default_value=r_kinematics_file),
    ]

    # Robot description from xacro
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]),
        ' ',
        LaunchConfiguration('urdf'),
        ' transmission_hw_interface:=', LaunchConfiguration('transmission_hw_interface'),
        ' kinematics_config_left:=', LaunchConfiguration('kinematics_config_left'),
        ' kinematics_config_right:=', LaunchConfiguration('kinematics_config_right'),
    ])
    robot_description = {'robot_description': robot_description_content}


    return LaunchDescription(declared_args + [
    Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[robot_description]
    ),
    ])

