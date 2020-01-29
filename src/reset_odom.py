#!/usr/bin/env python
import rospy
import socket
import struct

porta = 3003
ipmyrio = '192.168.1.100'

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ipmyrio, porta)
    client.connect(server_address)

    rospy.init_node('myrio_reset_odom', anonymous=False)
    rospy.loginfo("Resetando Odometria ...")
    data = client.recv(4)
    codigo = struct.unpack('>i', data)[0]
    if codigo:
        rospy.loginfo("Odometria resetada")
    else:
        rospy.logerr("ERRO AO RESETAR A ODOMETRIA")

except (KeyboardInterrupt,SystemExit,socket.error):
    client.close()