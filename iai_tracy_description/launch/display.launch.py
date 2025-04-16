import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import FindExecutable


def generate_launch_description():
    # Declare arguments
    urdf_arg = DeclareLaunchArgument(
        name='urdf',
        default_value=os.path.join(
            get_package_share_directory('iai_tracy_description'),
            'urdf',
            'tracy.urdf.xacro'
        )
    )

    transmission_hw_interface_arg = DeclareLaunchArgument(
        name='transmission_hw_interface',
        default_value='hardware_interface/PositionJointInterface'
    )

    kinematics_config_left_arg = DeclareLaunchArgument(
        name='kinematics_config_left',
        default_value=os.path.join(
            get_package_share_directory('iai_tracy_ur'),
            'include',
            'iai_tracy_ur',
            'left_ur10e_calibration.yaml'
        )
    )

    kinematics_config_right_arg = DeclareLaunchArgument(
        name='kinematics_config_right',
        default_value=os.path.join(
            get_package_share_directory('iai_tracy_ur'),
            'include',
            'iai_tracy_ur',
            'right_ur10e_calibration.yaml'
        )
    )

    kinematics_params_arg = DeclareLaunchArgument(
        name='kinematics_params',
        default_value=os.path.join(
            get_package_share_directory('ur_description'),
            'config',
            'ur5',
            'default_kinematics.yaml'
        )
    )

    # Robot description using xacro + args
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]),
        ' ',
        LaunchConfiguration('urdf'),
        ' transmission_hw_interface:=', LaunchConfiguration('transmission_hw_interface'),
        ' kinematics_config_left:=', LaunchConfiguration('kinematics_config_left'),
        ' kinematics_config_right:=', LaunchConfiguration('kinematics_config_right'),
    ])
    robot_description = {'robot_description': robot_description_content}

    # RViz config path
    rviz_file = os.path.join(
        get_package_share_directory('iai_tracy_description'),
        'rviz2',
        'display.rviz'
    )

    return LaunchDescription([
        # Declare launch arguments
        urdf_arg,
        transmission_hw_interface_arg,
        kinematics_config_left_arg,
        kinematics_config_right_arg,
        kinematics_params_arg,

        # Nodes
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
            output='log'
        )
    ])
