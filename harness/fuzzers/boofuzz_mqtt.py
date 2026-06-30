#!/usr/bin/env python3
import os
from boofuzz import (
    Session,
    Target,
    TCPSocketConnection,
    s_initialize,
    s_block_start,
    s_block_end,
    s_byte,
    s_size,
    s_word,
    s_static,
    s_string,
    s_get,
)

MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")


def define_connect():
    s_initialize(name="mqtt_connect")

    # CONNECT fixo e válido.
    # Remaining Length correto: 0x11 = 17 bytes.
    s_static(b"\x10\x11\x00\x04MQTT\x04\x02\x00\x3c\x00\x05DARLA")


def define_publish():
    s_initialize(name="mqtt_publish")

    # PUBLISH QoS 0
    s_byte(0x30, name="publish_packet_type", fuzzable=False)

    # Remaining length calculado sobre topic length + topic + payload.
    s_size(
        block_name="publish_body",
        length=1,
        endian="big",
        fuzzable=False,
        name="publish_remaining_length",
    )

    if s_block_start("publish_body"):
        topic_bytes = MQTT_TOPIC.encode("utf-8")

        s_word(len(topic_bytes), endian="big", fuzzable=False)
        s_static(MQTT_TOPIC)

        # Payload fuzzado. Mantemos curto para caber em Remaining Length de 1 byte.
        s_string(
            '{"temperature": 22.5}',
            name="payload",
            fuzzable=True,
            max_len=60,
        )

    s_block_end()


def main():
    print(f"[BOOFUZZ] Broker: {MQTT_HOST}:{MQTT_PORT}")
    print(f"[BOOFUZZ] Topic: {MQTT_TOPIC}")

    connection = TCPSocketConnection(MQTT_HOST, MQTT_PORT)

    session = Session(
        target=Target(connection=connection),
        web_port=None,
        receive_data_after_fuzz=True,
        ignore_connection_reset=True,
        ignore_connection_aborted=True,
        sleep_time=0.05,
    )

    define_connect()
    define_publish()

    # O BooFuzz enviará CONNECT válido antes do PUBLISH.
    session.connect(s_get("mqtt_connect"))
    session.connect(s_get("mqtt_connect"), s_get("mqtt_publish"))

    session.fuzz()


if __name__ == "__main__":
    main()