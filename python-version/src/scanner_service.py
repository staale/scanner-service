#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="staaleu"
__date__ ="$Oct 4, 2009 11:50:43 AM$"

import atexit
import sane
import time

import daemon
import logging
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "imagetagger.settings"

from imagetagger import local_settings
from imagetagger.handle.models import ImageFile

logging.basicConfig(filename=local_settings.LOG_FILENAME,level=logging.DEBUG,)

log = logging.getLogger('scanner-service')
log.setLevel(logging.DEBUG)


def open_device():
    dev_list = sane.get_devices()
    for i in range(len(dev_list)):
        dev_info = dev_list[i]
        log.info("Found device, vendor: %s, name: %s"%(dev_info[1], dev_info[2]))
        if "CANON" == dev_info[1] and "MP610" in dev_info[2]:
            log.info("Using device: %s"%dev_info[0])
            dev = sane.open(dev_info[0])
            dev.resolution = 300
            dev.button_controlled = True
            log.info("Setting resolution to %d, button controlled is enabled"%dev.resolution)
            return dev

def main():
    sane.init()
    img_count = 1
    try:
        dev = open_device()
        def close_scanner():
            log.info("Closing scanner")
            dev.close()
        atexit.register(close_scanner)
        log.info("Scanner service started, press button to scan images")
        while True:
            dev.start()
            log.debug("Please press scan button")
            img = dev.snap()
            filename = "img-%s-%05d.jpg"%(time.strftime("%Y-%m-%d-%H%M%S"), img_count%100000)
            img.save(os.path.join(local_settings.OUTPUT_FOLDER, filename), quality=100)
            img_file = ImageFile(path=filename)
            img_file.save()
            img_count += 1
            log.info("Saved image to %s - id: %d"%(filename, img_file.id))
    finally:
        log.info("Closing scanner service")
        sane.exit()

if __name__ == "__main__":
    with daemon.DaemonContext():
        main()