ARG ROS_DISTRO=humble
ARG PREFIX=

FROM husarnet/ros:${PREFIX}${ROS_DISTRO}-ros-core

RUN apt update && apt install -y \
      ros-${ROS_DISTRO}-apriltag-ros \
      ros-${ROS_DISTRO}-v4l2-camera \
      ros-${ROS_DISTRO}-image-transport-plugins \
      ros-${ROS_DISTRO}-nav2-common \
      ros-${ROS_DISTRO}-image-proc && \
    apt clean &&  \
    rm -rf /var/lib/apt/lists/*

COPY ./husarion_utils /husarion_utils

RUN echo $(dpkg -s ros-$ROS_DISTRO-apriltag-ros | grep 'Version' | sed -r 's/Version:\s([0-9]+.[0-9]+.[0-9]+).*/\1/g') > /version.txt
