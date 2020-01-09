#!/usr/bin/env python
import rospy
import socket
import struct
import json
from rospy_message_converter.json_message_converter import convert_ros_message_to_json as ros2json
import geometry_msgs.msg
from geometry_msgs.msg import Twist

porta = 3002
ipmyrio = '192.168.1.100'
looprate = 50
nomedotopico = '/cmd_vel'
cmd_vel_ros = Twist()

def callback(data):
    cmd_vel_ros = data.data

cmd_vel_ros.linear.z = 50

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ipmyrio, porta)
client.connect(server_address)

rospy.init_node('myrio_cmd_vel', anonymous=False)
rospy.loginfo("Conectado ao myRIO (%s) na porta %d",ipmyrio, porta)

sub = rospy.Subscriber(nomedotopico, Twist, callback)
rate = rospy.Rate(looprate) # Hz
rospy.loginfo("Inscrito no topico /%s ...", nomedotopico)

while not rospy.is_shutdown():
    dado_json = ros2json(cmd_vel_ros)
    client.sendall(struct.pack('>i', len(dado_json))+dado_json)
    rate.sleep()