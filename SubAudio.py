import logging
import asyncio
import numpy as np
import wave

from pygame.locals import *
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from pyaudio import PyAudio, paInt16

#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#
SAMPLING_RATE = 8000
po = PyAudio()
ostream = po.open(format=paInt16, channels=1, rate=SAMPLING_RATE, output=True)


@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1:1883/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    yield from C.subscribe([
                ('/test/audio', QOS_2),
             ])
    logger.info("Subscribed")
    try:
        while(True):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            ostream.write(packet.payload.data)
            #print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['/test/audio', ])
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
