import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import socket
import numpy as np

class ImageServer(Node):
    def __init__(self):
        super().__init__('image_server')
        self.br = CvBridge()

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16384)  

        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10)  
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]  
    def image_callback(self, msg):
        try:
 
            frame = self.br.imgmsg_to_cv2(msg, "bgr8")

            frame = cv2.resize(frame, (640, 480))  
            result, encoded_frame = cv2.imencode('.jpg', frame, self.encode_param)

            if not result:
                self.get_logger().warn("图像编码失败")
                return

            data = encoded_frame.tobytes()

            for i in range(0, len(data), 65507):  
                self.udp_socket.sendto(data[i:i+65507], ('<client_ip>', 8888))  

        except Exception as e:
            self.get_logger().error(f"发送图像数据时出错: {e}")

    def destroy_node(self):
        self.udp_socket.close() 
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    image_server = ImageServer()

    try:
        rclpy.spin(image_server)
    except KeyboardInterrupt:
        image_server.get_logger().info("程序中断，关闭连接...")
    finally:
        image_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
