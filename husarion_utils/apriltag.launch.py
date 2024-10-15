# Copyright 2024 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from nav2_common.launch import ReplaceString


def generate_launch_description():
    use_sim = LaunchConfiguration("use_sim")
    declare_use_sim_arg = DeclareLaunchArgument(
        "use_sim",
        default_value="False",
        description="Whether simulation is used",
        choices=["True", "False"],
    )

    namespace = LaunchConfiguration("namespace")
    declare_namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Add namespace to all launched nodes.",
    )

    apriltag_config_path = LaunchConfiguration("apriltag_config_path")
    apriltag_config_path_arg = DeclareLaunchArgument(
        "apriltag_config_path",
        default_value=PathJoinSubstitution(
            [FindPackageShare("panther_docking"), "config", "apriltag.yaml"]
        ),
        description=("Path to apriltag configuration file."),
    )

    camera_image_topic = LaunchConfiguration("camera_image_topic")
    declare_camera_image_topic_arg = DeclareLaunchArgument(
        "camera_image_topic",
        default_value="/camera/color/image_raw",
        description="Image topic from camera",
    )

    camera_info_topic = LaunchConfiguration("camera_info_topic")
    declare_camera_info_topic_arg = DeclareLaunchArgument(
        "camera_info_topic",
        default_value="/camera/color/camera_info",
        description="Camera info topic",
    )

    apriltag_detections_topic = LaunchConfiguration("apriltag_detections_topic")
    declare_apriltag_detections_topic_arg = DeclareLaunchArgument(
        "apriltag_detections_topic",
        default_value="/docking/april_tags",
        description="Topic to publish apriltag detections",
    )

    namespaced_apriltag_config_path = ReplaceString(
        source_file=apriltag_config_path,
        replacements={"<robot_namespace>": namespace, "//": "/"},
    )

    return LaunchDescription(
        [
            declare_use_sim_arg,
            declare_namespace_arg,
            declare_camera_image_topic_arg,
            declare_camera_info_topic_arg,
            declare_apriltag_detections_topic_arg,
            apriltag_config_path_arg,
            Node(
                package="apriltag_ros",
                executable="apriltag_node",
                parameters=[{"use_sim_time": use_sim}, namespaced_apriltag_config_path],
                namespace=namespace,
                emulate_tty=True,
                remappings={
                    "camera_info": camera_info_topic,
                    "image_rect": camera_image_topic,
                    "detections": apriltag_detections_topic,
                }.items(),
            ),
        ]
    )
