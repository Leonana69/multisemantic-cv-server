import json
import cv2
import numpy as np

# packet = {
#     'user': 'guojun',
#     'mode': 'single-image',
#     'width': 800,
#     'height': 601,
#     'ch': 3,
#     'fps': -1,
#     'function': 'pose',
#     'image': "...",
# }

class MultisemanticPacket():
    mode = ['single-image', 'stream']
    function = ['pose', 'slam', 'face', 'hands']

    def default_server_packet(client_packet):
        r_packet = {
            'user': client_packet['user'],
            'mode': client_packet['mode'],
            'function': client_packet['function'],
            'status': '',
            'result': '',
        }
        return r_packet

    def parse(str_info):
        is_valid_packet = True
        json_packet = json.loads(str_info)

        for f in json_packet['function']:
            if f in MultisemanticPacket.function:
                print("[P] valid function: {}".format(f))
            else:
                print("[P] invalid function: {}".format(f))
                is_valid_packet = False

        if json_packet['mode'] in MultisemanticPacket.mode:
            print("[P] valid mode: {}".format(json_packet['mode']))
        else:
            print("[P] valid mode: {}".format(json_packet['mode']))
            is_valid_packet = False

        img = np.array(json_packet['image'], dtype=np.uint8)
        recovered_image = cv2.imdecode(img, cv2.IMREAD_COLOR)
        if recovered_image.any():
            print("[P] image: {}".format(recovered_image.shape))
        else:
            print("[P] no image")

        packet = MultisemanticPacket.default_server_packet(json_packet)

        if is_valid_packet and recovered_image.any():
            return (packet, recovered_image)
        else:
            return (packet, None)