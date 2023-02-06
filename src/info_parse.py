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
    def info_parse(str_info):

        is_valid_packet = True
        json_packet = json.loads(str_info)

        for f in json_packet['function']:
            if f in MultisemanticPacket.function:
                print("---> valid function: {}".format(f))
            else:
                print("xxx> invalid function: {}".format(f))
                is_valid_packet = False

        if json_packet['mode'] in MultisemanticPacket.mode:
            print("---> valid mode: {}".format(json_packet['mode']))
        else:
            print("xxx> valid mode: {}".format(json_packet['mode']))
            is_valid_packet = False

        img = np.array(json_packet['image'], dtype=np.uint8)
        recovered_image = cv2.imdecode(img, cv2.IMREAD_COLOR)
        if recovered_image.any():
            print("---> image: {}".format(recovered_image.shape))
        else:
            print("xxx> no image")

        if is_valid_packet and recovered_image.any():
            return (json_packet, recovered_image)
        else:
            return (None, None)