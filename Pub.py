import logging
import asyncio
import pygame
import pygame.camera
import time

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import *


#
# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows
#

logger = logging.getLogger(__name__)
pygame.camera.init()
cam = pygame.camera.Camera('/dev/video0',(640,480))
cam.start()

config = {
    'will': {
        'topic': '/will/client',
        'message': b'Dead or alive',
        'qos': 0x01,
        'retain': True
    }
}

'''
@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1:1883/')
    tasks = [
        asyncio.ensure_future(C.publish('/test', b'TEST MESSAGE WITH QOS_0')),
        asyncio.ensure_future(C.publish('/test', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
        asyncio.ensure_future(C.publish('/test', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()
'''


@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://127.0.0.1:1883/')
        while(True):
            #message = yield from C.publish('/test', b'TEST MESSAGE WITH QOS_0', qos=0x00)
            #message = yield from C.publish('/test', b'TEST MESSAGE WITH QOS_1', qos=0x01)
            string = pygame.image.tostring(cam.get_image(),"RGB")
            message = yield from C.publish('/test', string, qos=0x02)
            time.sleep(0.1)
        #print(message)
        #logger.info("messages published")
        yield from C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter = "%(message)s"
    #logging.basicConfig(level=logging.DEBUG, format=formatter)
    #asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_until_complete(test_coro2())
