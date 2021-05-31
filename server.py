import io
import socket
import struct
from PIL import Image

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces) (192.168.4.43)

server_socket = socket.socket()
host = socket.gethostname()
host = '192.168.10.172'
server_socket.bind((host, 8000))
server_socket.listen(0)
print('socket up: ', host)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
print('connection found: ', connection)
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(4))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        image.save('test.jpg')
        image.verify()
        print('Image is verified')
finally:
    print('socket closed')
    connection.close()
    server_socket.close()
