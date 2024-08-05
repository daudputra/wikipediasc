import s3fs
import logging

logger = logging.getLogger(__name__)
def upload_to_s3(local_path, raw_path):
    client_kwargs = {
        'key': 'GLZG2JTWDFFSCQVE7TSQ',
        'secret': 'VjTXOpbhGvYjDJDAt2PNgbxPKjYA4p4B7Btmm4Tw',
        'endpoint_url': 'http://10.12.1.149:8000',

        'anon': False
    }
    
    s3 = s3fs.core.S3FileSystem(**client_kwargs)
    s3.upload(rpath=raw_path, lpath=local_path)
    if s3.exists(raw_path):
        logger.info('File upload successfully')
    else:
        logger.info('File upload failed')  