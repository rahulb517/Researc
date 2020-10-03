import os
import datetime
import time
from PIL import Image

import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token
    
    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def stitch(images, dt_string, path):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    
    name = path + dt_string + 'combined.jpg'
    new_im.save(name)
    return name


def main():
    dt = datetime.datetime.now()
    dt_string = dt.strftime("%d-%m-%Y,%H:%M:%S")
    fname1 = dt_string + '1' + '.jpg'
    fname2 = dt_string + '2' + '.jpg'
    fname3 = dt_string + '3' + '.jpg'
    
    path = '/home/pi/Pictures/test/'

    os.system('fswebcam -d /dev/video0 -r 1920x1080 --save ' + path + fname1)
    os.system('fswebcam -d /dev/video2 -r 1920x1080 --save ' + path + fname2)
    os.system('fswebcam -d /dev/video4 -r 1920x1080 --save ' + path + fname3)

    
    images = [Image.open(x) for x in [path + fname1, path + fname2, path + fname3]]
    name = stitch(images, dt_string, path)

    
    access_token = ' ' #unique token for dropbox account
    transferData = TransferData(access_token)
    file_from = name
    file_to = '/Photos/' + dt_string + '.jpg'

    transferData.upload_file(file_from, file_to)

if __name__ == '__main__':
    while(1):
        main()
        time.sleep(15) #take photo at this interval



