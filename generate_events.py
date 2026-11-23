#!/usr/bin/env python3
"""
Генерация тестового набора данных событий информационной безопасности
в формате JSON (events.json) для последующего анализа.

Имитирует упрощённый лог событий IDS/IPS-системы (в духе Suricata/Snort):
каждое событие имеет метку времени, тип сигнатуры (signature),
уровень серьёзности, протокол, src/dst IP и порт.
"""

import json
import random
from datetime import datetime, timedelta

random.seed(42)

SIGNATURES = [
    "ET SCAN Nmap Scripting Engine User-Agent Detected",
    "ET POLICY SSH session in progress on Unusual Port",
    "ET MALWARE Possible Windows executable sent when remote host claims to send an image",
    "ET EXPLOIT Possible SQL Injection Attempt",
    "ET WEB_SERVER Possible XSS Attempt in URI",
    "ET SCAN Potential SSH Scan",
    "ET TROJAN Generic Trojan Callback Detected",
    "ET POLICY Suspicious inbound to mySQL port",
    "ET DOS Possible NTP DDoS Inbound",
    "ET INFO Executable Download from dotted-quad Host",
    "ET WEB_CLIENT Possible CVE Exploit Attempt",
    "ET ATTACK_RESPONSE Possible Credential Dump Attempt",
]

PROTOCOLS = ["TCP", "UDP", "ICMP"]
SEVERITIES = [1, 2, 3]

# Задаём разную "популярность" сигнатур, чтобы распределение было неравномерным
WEIGHTS = [25, 8, 5, 18, 14, 10, 6, 4, 3, 9, 7, 6]

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def generate_events(n=1200):
    events = []
    start = datetime(2026, 11, 1, 0, 0, 0)
    for i in range(n):
        ts = start + timedelta(seconds=random.randint(0, 20 * 24 * 3600))
        sig = random.choices(SIGNATURES, weights=WEIGHTS, k=1)[0]
        event = {
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S"),
            "event_type": "alert",
            "src_ip": random_ip(),
            "src_port": random.randint(1024, 65535),
            "dest_ip": random_ip(),
            "dest_port": random.choice([22, 80, 443, 3306, 3389, 8080, 53]),
            "proto": random.choice(PROTOCOLS),
            "signature": sig,
            "severity": random.choice(SEVERITIES),
        }
        events.append(event)
    return events

if __name__ == "__main__":
    data = generate_events(1200)
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сгенерировано {len(data)} событий -> events.json")
