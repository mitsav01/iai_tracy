import launch
import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.parameter_descriptions import Parameter

def generate_launch_description():

    kinematics_config_left = os.path.join(get_package_share_directory('iai_tracy_ur'),'include','iai_tracy_ur','left_ur10e_calibration.yaml')
    kinematics_config_right = os.path.join(get_package_share_directory('iai_tracy_ur'),'include','iai_tracy_ur','right_ur10e_calibration.yaml')

    return LaunchDescription([

        # Include the iai_tracy_description launch file
        Node(
            package='iai_tracy_description',
            executable='display.launch.py',
            name='upload_description',
            parameters=[
                {'kinematics_config_left': kinematics_config_left, 'kinematics_config_right': kinematics_config_right}
            ]
        ),
        
        # Include the ur_robot_driver for the left arm
        Node(
            package='ur_robot_driver',
            executable='ur10e.launch.py',
            namespace='left_arm',
            arguments=[
                'robot_ip:=192.168.102.154',
                'tf_prefix:=left_',
                'controller_config_file:=$(find iai_tracy_ur)/config/ur10e_controllers_left.yaml',
                'controllers:=joint_state_controller_left scaled_pos_joint_traj_controller_left',
                'stopped_controllers:=pos_joint_traj_controller_left',
                'kinematics_config:=$(arg kinematics_config_left)',
                'robot_description_file:=$(find iai_tracy_description)/launch/display.launch.py',
                'reverse_port:=50011',
                'script_sender_port:=50012',
                'trajectory_port:=50013',
                'script_command_port:=50014'
            ]
        ),
        
        # Include the ur_robot_driver for the right arm
        Node(
            package='ur_robot_driver',
            executable='ur10e.launch.py',
            namespace='right_arm',
            arguments=[
                'robot_ip:=192.168.102.153',
                'tf_prefix:=right_',
                'controller_config_file:=$(find iai_tracy_ur)/config/ur10e_controllers_right.yaml',
                'controllers:=joint_state_controller_right scaled_pos_joint_traj_controller_right',
                'stopped_controllers:=pos_joint_traj_controller_right',
                'kinematics_config:=$(arg kinematics_config_right)',
                'robot_description_file:=$(find iai_tracy_description)/launch/display.launch.py',
                'reverse_port:=50001',
                'script_sender_port:=50002',
                'trajectory_port:=5003',
                'script_command_port:=50005'
            ]
        ),

        # Gripper nodes for the right and left grippers
        Node(
            package='robotiq_2f_gripper_control',
            executable='Robotiq2FGripperRtuNode.py',
            name='right_gripper_driver',
            arguments=['/dev/ttyUSB0'],
            namespace='right_gripper'
        ),
        
        Node(
            package='robotiq_2f_gripper_control',
            executable='Robotiq2FGripperRtuNode.py',
            name='left_gripper_driver',
            arguments=['/dev/ttyUSB1'],
            namespace='left_gripper'
        ),

        # Gripper action server nodes
        Node(
            package='robotiq_2f_gripper_action_server',
            executable='robotiq_2f_gripper_action_server_node',
            name='gripper_action_server_right',
            parameters=[{'gripper_name': 'right_gripper'}],
            remappings=[
                ('input', '/right_gripper/Robotiq2FGripperRobotInput'),
                ('output', '/right_gripper/Robotiq2FGripperRobotOutput')
            ]
        ),

        Node(
            package='robotiq_2f_gripper_action_server',
            executable='robotiq_2f_gripper_action_server_node',
            name='gripper_action_server_left',
            parameters=[{'gripper_name': 'left'}],
            remappings=[
                ('input', '/left_gripper/Robotiq2FGripperRobotInput'),
                ('output', '/left_gripper/Robotiq2FGripperRobotOutput')
            ]
        ),

        # Joint state publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{
                'source_list': ['/left_arm/joint_states', '/right_arm/joint_states'],
                'rate': 120,
                'use_gui': False
            }],
            output='screen'
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen'
        ),
    ])