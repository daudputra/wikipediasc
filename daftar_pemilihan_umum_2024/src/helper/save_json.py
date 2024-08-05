import json
import os
from datetime import datetime

class SaveJson:

    def __init__(self, response, prov, title, tag:None, s3_path, data):
        self.response = response
        self.prov = prov
        self.title = title
        self.tag = tag
        self.s3_path = s3_path
        self.data:dict = data


    async def save_json_local(self, filename, provinsi):
        directory = os.path.join('data', provinsi.replace(' ', '_').lower())
        os.makedirs(directory, exist_ok=True)
        filename_json = filename.replace(' ', '_').lower()
        file_path = os.path.join(directory, filename_json)

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(await self.mapping(), json_file, ensure_ascii=False)


    async def mapping(self):
        full_data = {
            'link': self.response,
            'domain': self.response.split('/')[2],
            'tag': [
                self.response.split('/')[2],
                self.prov,
                self.tag
            ],
            'crawling_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crawling_time_epoch': int(datetime.now().timestamp()),
            'path_data_raw': self.s3_path,
            'path_data_clean': None,
            'provinsi_kabupaten_kota': self.prov,
            'title': self.title,
            'data': self.data
        }
        return full_data