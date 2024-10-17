import cv2
import socket
import numpy as np

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16384)


client_address = ('0.0.0.0', 8888)
udp_socket.bind(client_address)

data = b""

while True:

    while True:
        packet, _ = udp_socket.recvfrom(65507)  
        data += packet
        if len(packet) < 65507:  
            break


    frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)


    if frame is not None:
        cv2.imshow("Video Stream", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

udp_socket.close()
cv2.destroyAllWindows()
