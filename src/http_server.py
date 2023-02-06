from http.server import BaseHTTPRequestHandler
from multisemantic_packet import MultisemanticPacket
import time
from pose_task import PoseTask
import json
import urllib
import cgi
import threading

class MultisemanticHTTPServerHandler(BaseHTTPRequestHandler):
    __pose_task = PoseTask()
    def set_html_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def set_json_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # the do_GET name is mandatory
    def do_GET(self):
        self.set_html_headers()
        with open('./assets/html/index.html') as f:
            self.wfile.write(bytes(f.read(), "utf-8"))

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        print("get post")
        # print(self.data_string)
        # (json_packet, img) = MultisemanticPacket.info_parse(self.data_string)

        # packet = {
        #     'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        #     'user': json_packet['user'],
        #     'mode': json_packet['mode'],
        #     'function': json_packet['function'],
        #     'result': '',
        # }

        # if img.any():
        #     result = MultisemanticHTTPServerHandler.__pose_task.run(img)
        #     packet['result'] = result.tolist()

        # self.set_json_headers()
        # self.wfile.write(bytes(json.dumps(packet), "utf-8"))
    
    # contentRoot = "."
    # uploadUrlPath = "/files"
    # def do_GET(self):
    #     parsed_path = self.path
    #     print(parsed_path)

    #     try:
    #         file_data = self.__retrieve_image(parsed_path)
    #         file_data_len = len(file_data)

    #     except Exception as ex:
    #         print("Runtime Error: ", ex)
    #         self.send_error(404)
    #         self.end_headers()
    #         self.wfile.write("File not found")
    #         return
    #     else:
    #         content_type = self.__find_out_content_type(parsed_path)
    #         print(content_type)
    #         self.send_response(200)
    #         self.send_header("Accept-Ranges", "bytes")
    #         self.send_header("Content-Disposition", "attachment")
    #         self.send_header("Content-Length", file_data_len)
    #         self.send_header("Content-type", content_type)
    #         self.end_headers()
    #         self.wfile.write(file_data)

    #     return



    # def __find_out_content_type(self, url_path):
    #     pieces = url_path.rsplit(".", 1)
    #     print(pieces)
    #     file_extention = pieces[1]
    #     if file_extention == "gif":
    #         return "image/gif"
    #     elif file_extention in ["jpeg","jpe","jpg", "jif","jfif","jfi"]:
    #         return "image/jpeg"
    #     elif file_extention == "png":
    #         return "image/png"
    #     elif file_extention in ["svg", "svgz"]:
    #         return "image/svg+xml"
    #     elif file_extention in ["tiff","tif"]:
    #         return "image/tiff"
    #     elif file_extention == ".ico":
    #         return "image/vnd.microsoft.icon"
    #     elif file_extention == ".wbmp":
    #         return "image/vnd.wap.wbmp"
    #     else:
    #         return "text/plain"

    # def __retrieve_image(self,url_path):
    #     image_path = self.__class__.contentRoot + url_path
    #     try:
    #         file = open(image_path,"rb")
    #     except IOError as ioerr:
    #         print("File not found : ", ioerr)
    #     else:
    #         file_data = file.read()
    #         file.close()
    #     return file_data

    # def do_POST(self):
    #     form = cgi.FieldStorage(
    #         fp = self.rfile,
    #         headers = self.headers,
    #         environ = { 'REQUEST_METHOD' : 'POST',
    #                   'CONTENT_TYPE' : self.headers['Content-Type'],
    #         })

    #     response_msg = None
        
    #     for field in form.keys():
    #         field_item = form[field]
    #         if field_item.filename:
    #             # field contains an uploaded file
    #             print("\n ********** \n")
    #             print(field_item.filename)
    #             file_data = field_item.file.read()
    #             file_len = len(file_data)
    #             print(file_len)
    #             try:
    #                 self.__save_image(file_data)
    #             except Exception as ex:
    #                 print("Runtime Error: ", ex)
    #                 self.send_error(500)
    #                 self.end_headers()
    #                 self.wfile.write("Can not upload file to server")
    #                 return
    #             else:
    #                 response_msg = "File uploaded"
    #         else:
    #             # regular form value
    #             self.wfile.write('\t%s=%s\n' % (field, form[field].value))

    #     # building successful response
    #     self.send_response(200)
    #     self.end_headers()
    #     self.wfile.write(response_msg)

    #     return

    # def __save_image(self, file_data):
    #     parsed_path = urllib.parse(self.path)

    #     import os
    #     path_to_upload_file = self.__class__.contentRoot + parsed_path.path
    #     result = path_to_upload_file.rsplit("/",1)
    #     print(result)
    #     path_to_create_dir = result[0]
    #     try:
    #         os.makedirs(path_to_create_dir)
    #     except OSError as oserror:
    #         print("Error while creation path to upload file ", oserror)

    #     try:
    #        file = open(path_to_upload_file,"wb")
    #     except IOError as ioerror:
    #         print("Can not open file: ", ioerror)
    #         raise Exception("Can not save file on server",)
    #     else:
    #         file.write(file_data)
    #         file.close()
    #         print("file closed")

    #     return
