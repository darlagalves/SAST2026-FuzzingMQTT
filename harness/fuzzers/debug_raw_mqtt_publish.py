#!/usr/bin/env python3
import os
import socket
import time

MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")
MQTT_PAYLOAD = '{"temperature": 77.7}'


def encode_remaining_length(length: int) -> bytes:
    encoded = bytearray()
    while True:
        digit = length % 128
        length //= 128
        if length > 0:
            digit |= 128
        encoded.append(digit)
        if length == 0:
            break
    return bytes(encoded)


def connect_packet() -> bytes:
    client_id = b"DARLA_DEBUG"
    variable_header = b"\x00\x04MQTT\x04\x02\x00\x3c"
    payload = len(client_id).to_bytes(2, "big") + client_id
    body = variable_header + payload
    return b"\x10" + encode_remaining_length(len(body)) + body


def publish_packet(topic: str, payload: str) -> bytes:
    topic_b = topic.encode("utf-8")
    payload_b = payload.encode("utf-8", errors="replace")
    body = len(topic_b).to_bytes(2, "big") + topic_b + payload_b
    return b"\x30" + encode_remaining_length(len(body)) + body


with socket.create_connection((MQTT_HOST, MQTT_PORT), timeout=3) as s:
    s.sendall(connect_packet())
    connack = s.recv(4)
    print(f"CONNACK: {connack!r}")

    s.sendall(publish_packet(MQTT_TOPIC, MQTT_PAYLOAD))
    print(f"Publicado em {MQTT_TOPIC}: {MQTT_PAYLOAD}")

    time.sleep(1)
