SITE_NAME = 'Hexchan'


DATE_TIME_FORMAT = 'd.m.Y в H:i:s'


# CAPTCHA_ENABLED = False


# Cache
CACHE_ENABLED = False
CACHE_POST_POPUP = 60 * 10  # 10 min
CACHE_START_PAGE = 60 * 10  # 10 min


# Images
IMAGE_EXTENSION = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif'}
IMAGE_CHUNK_SIZE = 1 * (1024 * 1024)  # 1 MiB
IMAGE_THUMB_SIZE = 200, 200


# Thumbs
THUMB_EXTENSION = 'png'
THUMB_TYPE = 'PNG'


# Uploads
FILE_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']
FILE_MAX_SIZE = 1 * (1024 * 1024)  # 1 MiB
FILE_MAX_NUM = 4


# HIDs
THREAD_HID_FORMAT = '0x{hid:06x}'
THREAD_HID_REGEX = '0x[0-9a-f]{6}'
THREAD_FULL_HID_FORMAT = '0x{hid:06x}'

POST_HID_FORMAT = '0x{hid:06x}'
POST_HID_REGEX = '0x[0-9a-f]{6}'
POST_FULL_HID_FORMAT = '0x{hid:06x}'

IMAGE_HID_FORMAT = '0x{hid:08x}'


# Posting limits
POSTING_TIMEOUT = 60  # seconds
