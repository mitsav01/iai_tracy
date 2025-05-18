from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():

    #Initialize config files

    left_kinematics_params = PathJoinSubstitution(
        [FindPackageShare("iai_tracy_ur"),"include","iai_tracy_ur","left_ur10e_calibration.yaml"]
    )
    left_controller_fl = PathJoinSubstitution(
        [FindPackageShare("iai_tracy_ur"),"config","ur10e_controllers_left.yaml"]
    )
    right_kinematics_params = PathJoinSubstitution(
        [FindPackageShare("iai_tracy_ur"),"include","iai_tracy_ur","right_ur10e_calibration.yaml"]
    )
    right_controller_fl = PathJoinSubstitution(
        [FindPackageShare("iai_tracy_ur"),"config","ur10e_controllers_right.yaml"]
    )

    description_launch_fl = PathJoinSubstitution(
        [FindPackageShare("iai_tracy_description"),"launch","display.launch.py"]
    )

    ur_type = LaunchConfiguration('ur_type') 

    description_launch_file = LaunchConfiguration('description_launch_file')
    left_robot_ip = LaunchConfiguration('left_robot_ip') 
    left_controller_config_file = LaunchConfiguration('left_controller_config_file') 
    left_tf_prefix = LaunchConfiguration('left_tf_prefix') 
    left_script_command_port = LaunchConfiguration('left_script_command_port')
    left_trajectory_port = LaunchConfiguration('left_trajectory_port')
    left_reverse_port = LaunchConfiguration('left_reverse_port')
    left_script_sender_port = LaunchConfiguration('left_script_sender_port')
    left_controllers = LaunchConfiguration('left_controllers')
    left_stopped_controllers = LaunchConfiguration('left_stopped_controller')
    left_kinematic_config = LaunchConfiguration('left_kinematic_config')
    

    right_robot_ip = LaunchConfiguration('right_robot_ip') 
    right_controller_config_file = LaunchConfiguration('right_controller_config_file') 
    right_tf_prefix = LaunchConfiguration('right_tf_prefix') 
    right_script_command_port = LaunchConfiguration('right_script_command_port')
    right_trajectory_port = LaunchConfiguration('right_trajectory_port')
    right_reverse_port = LaunchConfiguration('right_reverse_port')
    right_script_sender_port = LaunchConfiguration('right_script_sender_port')
    right_controllers = LaunchConfiguration('right_controllers')
    right_stopped_controllers = LaunchConfiguration('right_stopped_controller')
    right_kinematic_config = LaunchConfiguration('right_kinematic_config')


    # # UR specific arguments
    ur_type_arg = DeclareLaunchArgument(
            "ur_type",
            default_value='ur10e',
            description="Type/series of used UR robot.",
            choices=["ur3", "ur3e", "ur5", "ur5e", "ur10", "ur10e", "ur16e", "ur20"],
    )
    description_launch_file_arg = DeclareLaunchArgument(
        "description_launch_file",
        default_value=description_launch_fl,
        description="publishes the description topic."
    )
    left_robot_ip_arg = DeclareLaunchArgument(
        "left_robot_ip",
        default_value='192.168.102.154',
        description="IP address by which the robot can be reached.",
    )
    left_tf_prefix_arg = DeclareLaunchArgument(
        "left_tf_prefix",
        default_value="left",
            description="tf_prefix of the joint names, useful for \
            multi-robot setup. If changed, also joint names in the controllers' configuration \
            have to be updated.",
    )
    left_controller_config_file_arg = DeclareLaunchArgument(
        "left_controller_config_file",
        default_value=left_controller_fl,
        description="YAML file with the controllers configuration.",
    )
    left_controllers_arg = DeclareLaunchArgument(
        "left_controllers",
        default_value="joint_state_controller_left scaled_pos_joint_traj_controller_left",
        description="controllers used in robot's operation",
    )
    left_stopped_controllers_arg = DeclareLaunchArgument(
        "left_stopped_controllers",
        default_value="pos_joint_traj_controller_left",
    )
    left_kinematic_config_arg = DeclareLaunchArgument(
        "left_kinematic_config",
        default_value=left_kinematics_params,
    )
    left_reverse_port_arg = DeclareLaunchArgument(
        "left_reverse_port",
        default_value="50011",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    left_script_sender_port_arg = DeclareLaunchArgument(
        "left_script_sender_port",
        default_value="50012",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    left_trajectory_port_arg = DeclareLaunchArgument(
        "left_trajectory_port",
        default_value="50013",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    left_script_command_port_arg = DeclareLaunchArgument(
        "left_script_command_port",
        default_value="50014",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )


    right_robot_ip_arg = DeclareLaunchArgument(
        "right_robot_ip",
        default_value='192.168.102.154',
        description="IP address by which the robot can be reached.",
    )
    right_tf_prefix_arg = DeclareLaunchArgument(
        "right_tf_prefix",
        default_value="right",
            description="tf_prefix of the joint names, useful for \
            multi-robot setup. If changed, also joint names in the controllers' configuration \
            have to be updated.",
    )
    right_controller_config_file_arg = DeclareLaunchArgument(
        "right_controller_config_file",
        default_value=right_controller_fl,
        description="YAML file with the controllers configuration.",
    )
    right_controllers_arg = DeclareLaunchArgument(
        "right_controllers",
        default_value="joint_state_controller_right scaled_pos_joint_traj_controller_right",
        description="controllers used in robot's operation",
    )
    right_stopped_controllers_arg = DeclareLaunchArgument(
        "right_stopped_controllers",
        default_value="pos_joint_traj_controller_right",
    )
    right_kinematic_config_arg = DeclareLaunchArgument(
        "right_linematic_config",
        default_value=right_kinematics_params,
    )
    right_reverse_port_arg = DeclareLaunchArgument(
        "right_reverse_port",
        default_value="50011",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    right_script_sender_port_arg = DeclareLaunchArgument(
        "right_script_sender_port",
        default_value="50012",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    right_trajectory_port_arg = DeclareLaunchArgument(
        "right_trajectory_port",
        default_value="50013",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )
    right_script_command_port_arg = DeclareLaunchArgument(
        "right_script_command_port",
        default_value="50014",
        description="Port that will be opened to forward script commands from the driver to the robot",
    )

    ur_launch_dir = get_package_share_directory('ur_robot_driver')

    left = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ur_launch_dir, 'launch', 'ur_control.launch.py')),
        launch_arguments={'ur_type': ur_type,
                          'robot_ip': left_robot_ip,
                          'controllers_file': left_controller_config_file,
                          'tf_prefix': left_tf_prefix,
                          'script_command_port': left_script_command_port,
                          'trajectory_port': left_trajectory_port,
                          'reverse_port': left_reverse_port,
                          'script_sender_port': left_script_sender_port,
                          'kinematic_params': left_kinematic_config,
                          'description_file': description_launch_file,

                          }.items())
    
    left_with_namespace = GroupAction(
     actions=[
         PushRosNamespace('left'),
         left
      ]
    )

    right = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ur_launch_dir, 'launch', 'ur_control.launch.py')),
        launch_arguments={'ur_type': ur_type,
                          'robot_ip': right_robot_ip,
                          'controllers_file': right_controller_config_file,
                          'tf_prefix': right_tf_prefix,
                          'script_command_port': right_script_command_port,
                          'trajectory_port': right_trajectory_port,
                          'reverse_port': right_reverse_port,
                          'script_sender_port': right_script_sender_port,
                          'kinematic_params': right_kinematic_config,
                          'description_file': description_launch_file,
                                                    
                          }.items())
    
    right_with_namespace = GroupAction(
     actions=[
         PushRosNamespace('right'),
         right
      ]
    )




    return LaunchDescription([
        ur_type_arg,
        description_launch_file_arg,
        left_robot_ip_arg,
        left_controller_config_file_arg,
        left_tf_prefix_arg,
        left_controllers_arg,
        left_stopped_controllers_arg,
        left_kinematic_config_arg,
        left_script_command_port_arg,
        left_trajectory_port_arg,
        left_reverse_port_arg,
        left_script_sender_port_arg,


        right_robot_ip_arg,
        right_controller_config_file_arg,
        right_tf_prefix_arg,
        right_controllers_arg,
        right_stopped_controllers_arg,
        right_kinematic_config_arg,
        right_script_command_port_arg,
        right_trajectory_port_arg,
        right_reverse_port_arg,
        right_script_sender_port_arg,


        left_with_namespace,
        right_with_namespace,
        # description_launch_file_arg
    ])
