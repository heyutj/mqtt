import logging
import asyncio
import numpy as np
import wave

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import *
from pyaudio import PyAudio, paInt16

#
# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows
#

NUM_SAMPLES = 2000
SAMPLING_RATE = 8000
pi = PyAudio()
istream = pi.open(format=paInt16, channels=1, rate=SAMPLING_RATE,
                  input=True, frames_per_buffer=NUM_SAMPLES)

@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://127.0.0.1:1883/')
        while(True):
            #message = yield from C.publish('/test', b'TEST MESSAGE WITH QOS_0', qos=0x00)
            #message = yield from C.publish('/test', b'TEST MESSAGE WITH QOS_1', qos=0x01)
            string_audio_data = istream.read(NUM_SAMPLES)
            message = yield from C.publish('/test/audio', string_audio_data, qos=0x02)
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
    asyncio.get_event_loop().run_until_complete(test_coro2())
