import logging
import asyncio
import pygame
import time
from pygame.locals import *
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

logger = logging.getLogger(__name__)
pygame.init()
SIZE = (640, 480)
display = pygame.display.set_mode(SIZE, 0)
screen = pygame.surface.Surface(SIZE, 0, display)

def on_display(image):
    display.blit(image, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN and event.key == K_s:
            pygame.image.save(image, FILENAME)
            pygame.quit()
    return

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1:1883/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    yield from C.subscribe([
                ('/test', QOS_2),
             ])
    logger.info("Subscribed")
    try:
        while(True):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            image = pygame.image.fromstring(bytes(packet.payload.data),SIZE,"RGB")
            on_display(image)
            #print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['/test', ])
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
