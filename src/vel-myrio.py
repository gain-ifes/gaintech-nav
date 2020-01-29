#!/usr/bin/env python
import rospy
import socket
import struct
import json
from rospy_message_converter.json_message_converter import convert_json_to_ros_message as json2ros
import geometry_msgs.msg
from geometry_msgs.msg import Twist

porta = 3001
ipmyrio = '192.168.1.100'
looprate = 50
nomedotopico = '/vel'
vel_ros = Twist()

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ipmyrio, porta)
    client.connect(server_address)

    rospy.init_node('myrio_vel', anonymous=False)
    rospy.loginfo("Conectado ao myRIO (%s) na porta %d",ipmyrio, porta)

    pub = rospy.Publisher(nomedotopico, Twist, queue_size=10)
    rate = rospy.Rate(looprate) # Hz
    rospy.loginfo("Publicando no topico /%s a %d Hz...", nomedotopico, looprate)
    while not rospy.is_shutdown():
        size = struct.unpack('>i', client.recv(4))[0]  # Extract the msg size from four bytes - mind the encoding
        dado_json = client.recv(size)
        vel_ros = json2ros('geometry_msgs/Twist', dado_json)
        pub.publish(vel_ros)
        rate.sleep()

except (KeyboardInterrupt,SystemExit,socket.error):
    client.close()