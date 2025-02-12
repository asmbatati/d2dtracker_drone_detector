from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    
    # Add argument for the path of the yaml file
    detection_yaml = LaunchConfiguration('detection_yaml')
    depth_topic = LaunchConfiguration('depth_topic')
    namespace = LaunchConfiguration('namespace')

    config = os.path.join(
        get_package_share_directory('d2dtracker_drone_detector'),
        'config',
        'detection_param.yaml'
    )
    
    detection_yaml_launch_arg = DeclareLaunchArgument(
        'detection_yaml',
        default_value=config
    )

    depth_topic_launch_arg = DeclareLaunchArgument(
        'depth_topic',
        default_value='interceptor/depth_image'
    )

    namespace_launch_arg = DeclareLaunchArgument(
        'namespace',
        default_value=''
    )

    # Detection node
    detection_node = Node(
        package='d2dtracker_drone_detector',
        executable='detection_node',
        name='detection_node',
        namespace=namespace,
        output='screen',
        parameters=[detection_yaml],
        remappings=[('interceptor/depth_image', depth_topic)]
    )

    ld = LaunchDescription()

    ld.add_action(detection_yaml_launch_arg)
    ld.add_action(depth_topic_launch_arg)
    ld.add_action(namespace_launch_arg)
    ld.add_action(detection_node)

    return ld