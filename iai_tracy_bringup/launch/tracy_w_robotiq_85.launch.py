import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch_ros.actions import Node, PushRosNamespace
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    iai_tracy_ur = get_package_share_directory('iai_tracy_ur')
    iai_tracy_description = get_package_share_directory('iai_tracy_description')
    ur_robot_driver = get_package_share_directory('ur_robot_driver')

    kinematics_config_left = os.path.join(iai_tracy_ur, 'include', 'iai_tracy_ur', 'left_ur10e_calibration.yaml')
    kinematics_config_right = os.path.join(iai_tracy_ur, 'include', 'iai_tracy_ur', 'right_ur10e_calibration.yaml')

    left_arm = GroupAction([
        PushRosNamespace('left_arm'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ur_robot_driver, 'launch', 'ur10e.launch.py')
            ),
            launch_arguments={
                'robot_ip': '192.168.102.154',
                'tf_prefix': 'left_',
                'controller_config_file': os.path.join(iai_tracy_ur, 'config', 'ur10e_controllers_left.yaml'),
                'controllers': 'joint_state_controller_left scaled_pos_joint_traj_controller_left',
                'stopped_controllers': 'pos_joint_traj_controller_left',
                'kinematics_config': kinematics_config_left,
                'robot_description_file': os.path.join(iai_tracy_description, 'launch', 'upload.launch.py'),
                'reverse_port': '50011',
                'script_sender_port': '50012',
                'trajectory_port': '50013',
                'script_command_port': '50014'
            }.items()
        )
    ])

    right_arm = GroupAction([
        PushRosNamespace('right_arm'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ur_robot_driver, 'launch', 'ur10e.launch.py')
            ),
            launch_arguments={
                'robot_ip': '192.168.102.153',
                'tf_prefix': 'right_',
                'controller_config_file': os.path.join(iai_tracy_ur, 'config', 'ur10e_controllers_right.yaml'),
                'controllers': 'joint_state_controller_right scaled_pos_joint_traj_controller_right',
                'stopped_controllers': 'pos_joint_traj_controller_right',
                'kinematics_config': kinematics_config_right,
                'robot_description_file': os.path.join(iai_tracy_description, 'launch', 'upload.launch.py'),
                'reverse_port': '50001',
                'script_sender_port': '50002',
                'trajectory_port': '50003',
                'script_command_port': '50005'
            }.items()
        )
    ])

    nodes = [
        # Upload robot description
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(iai_tracy_description, 'launch', 'upload.launch.py')
            ),
            launch_arguments={
                'kinematics_config_left': kinematics_config_left,
                'kinematics_config_right': kinematics_config_right
            }.items()
        ),

        left_arm,
        right_arm,

        # Robotiq Gripper Drivers
        Node(
            package='ros2_robotiq_gripper',
            executable='Robotiq2FGripperRtuNode.py',
            name='right_gripper_driver',
            namespace='right_gripper',
            arguments=['/dev/ttyUSB0']
        ),
        Node(
            package='ros2_robotiq_gripper',
            executable='Robotiq2FGripperRtuNode.py',
            name='left_gripper_driver',
            namespace='left_gripper',
            arguments=['/dev/ttyUSB1']
        ),

        # Gripper Action Servers
        Node(
            package='ros2_robotiq_gripper',
            executable='robotiq_2f_gripper_action_server_node',
            name='gripper_action_server_right',
            parameters=[{'gripper_name': 'right_gripper'}],
            remappings=[
                ('input', '/right_gripper/Robotiq2FGripperRobotInput'),
                ('output', '/right_gripper/Robotiq2FGripperRobotOutput')
            ]
        ),
        Node(
            package='ros2_robotiq_gripper',
            executable='robotiq_2f_gripper_action_server_node',
            name='gripper_action_server_left',
            parameters=[{'gripper_name': 'left'}],
            remappings=[
                ('input', '/left_gripper/Robotiq2FGripperRobotInput'),
                ('output', '/left_gripper/Robotiq2FGripperRobotOutput')
            ]
        ),

        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{
                'source_list': ['/left_arm/joint_states', '/right_arm/joint_states'],
                'rate': 120,
                'use_gui': False
            }]
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen'
        )
    ]

    return LaunchDescription(nodes)
