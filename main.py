import time
from datetime import datetime
from urllib.request import urlopen
import json
import requests
from path_url import Path_URL

path_file = Path_URL
path_url = path_file.path_local+"api/Rest_api/get_data_setting"
url_data_logger = path_file.path_server+"api/Data_logger/volt"
url_local_logger = path_file.path_local+"api/Data_logger/volt"
machine_code = ""

while True:
    try:
        read_machine_code = open("/home/pi/machine_code/machine_code.txt","r")
        machine_code = read_machine_code.read().rstrip('\n')
        if machine_code != '':
            response = urlopen(path_url)
            data_json = json.loads(response.read())
            if int(data_json[0]['online_status']) == 1:
                print("อัพโหลดไฟล์ แบบ online")
                # volt
                volt = open('/home/pi/hottub_ma/txt_file/volt_tag.txt','r')
                split_file_volt = volt.read().split(",")
                volt1 = split_file_volt[0].replace("[","")
                volt2 = split_file_volt[1]
                volt3 = split_file_volt[2].replace("]","")
                resp = requests.post(url_data_logger, data={
                                                            'va':volt1,
                                                            'vb':volt2,
                                                            'vc':volt3,
                                                            'machine_code':machine_code
                                                    })
                resp = requests.post(url_local_logger, data={
                                                            'va':volt1,
                                                            'vb':volt2,
                                                            'vc':volt3,
                                                            'machine_code':machine_code
                                                    })
                time.sleep(5)
            else:
                print("โหมด Offline")
                volt = open('/home/pi/hottub_ma/txt_file/volt_tag.txt','r')
                split_file_volt = volt.read().split(",")
                volt1 = split_file_volt[0].replace("[","")
                volt2 = split_file_volt[1]
                volt3 = split_file_volt[2].replace("]","")
                resp = requests.post(url_local_logger, data={
                                                            'va':volt1,
                                                            'vb':volt2,
                                                            'vc':volt3,
                                                            'machine_code':machine_code
                                                    })
                time.sleep(300)
        else:
            time.sleep(5)
    except:
        pass
   

   
