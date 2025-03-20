"""
MineDetector - Cryptocurrency Mining Detection Tool
Copyright (c) 2024 Loaris Cybersecurity Inc.
https://loaris.com

Description:
    MineDetector is an open-source tool designed to detect unauthorized cryptocurrency mining 
    (cryptojacking) on your system. It monitors CPU usage and network connections to identify 
    processes that may be engaging in mining activities without your consent.

License:
    MIT License
    See LICENSE file for more details.
"""

import psutil
import time
import socket
import datetime

# List of domains associated with cryptojacking
cryptojacking_domains = [
    "coinhive.com", "coin-hive.com", "jsecoin.com", "minemytraffic.com",
    "crypto-loot.com", "2giga.link", "ppoi.org", "coinerra.com", "coin-have.com",
    "kiwifarms.net", "anime.reactor.cc", "joyreactor.cc", "kissdoujin.com",
    "coinnebula.com", "afminer.com", "coinblind.com", "webmine.cz",
    "monerominer.rocks", "cdn.cloudcoins.co", "coinlab.biz", "papoto.com", 
    "cookiescript.info", "cookiescriptcdn.pro", "rocks.io", "ad-miner.com", 
    "party-nngvitbizn.now.sh", "cryptoloot.pro", "jscdndel.com", "mine.nahnoji.cz",
    "miner.cryptobara.com", "digger.cryptobara.com", "kickass.cd",    
    "coinpirate.cf", "a-o.ninja", "you.tubetitties.com",
    "hive.tubetitties.com", "sushipool.com", "eu.sushipool.com"
]

# List of legitimate mining pool domains
legitimate_pools = [
    "antpool.com", "f2pool.com", "viabtc.com", "pool.binance.com", "slushpool.com",
    "luxor.tech", "foundryusa.com", "btc.com", "poolin.com", "miningpoolhub.com",
    "ethermine.org", "nanopool.org", "2miners.com", "suprnova.cc", "nicehash.com",
    "emcd.io", "sbicrypto.com"
]

# Resolve domains to IP addresses and store in dictionaries
cryptojacking_ip_to_domain = {}
for domain in cryptojacking_domains:
    try:
        addr_info = socket.getaddrinfo(domain, None)
        for info in addr_info:
            ip = info[4][0]
            cryptojacking_ip_to_domain[ip] = domain
    except socket.gaierror:
        print(f"Warning: Could not resolve domain {domain}")

legitimate_ip_to_domain = {}
for domain in legitimate_pools:
    try:
        addr_info = socket.getaddrinfo(domain, None)
        for info in addr_info:
            ip = info[4][0]
            legitimate_ip_to_domain[ip] = domain
    except socket.gaierror:
        print(f"Warning: Could not resolve domain {domain}")

# Set CPU usage baseline for accurate measurements
for proc in psutil.process_iter():
    try:
        proc.cpu_percent(interval=None)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

print("Monitoring for suspicious mining activity... Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(10)  # Check every 10 seconds
        for proc in psutil.process_iter():
            try:
                cpu_usage = proc.cpu_percent(interval=None)
                if cpu_usage > 70:  # Threshold for high CPU usage
                    suspicious_connections = []
                    connections = proc.connections()
                    for conn in connections:
                        if conn.raddr:
                            ip = conn.raddr.ip
                            if ip in cryptojacking_ip_to_domain:
                                domain = cryptojacking_ip_to_domain[ip]
                                domain_type = "Cryptojacking Domain"
                                suspicious_connections.append((ip, domain, domain_type))
                            elif ip in legitimate_ip_to_domain:
                                domain = legitimate_ip_to_domain[ip]
                                domain_type = "Legitimate Mining Pool"
                                suspicious_connections.append((ip, domain, domain_type))
                    if suspicious_connections:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} Suspicious process detected:")
                        print(f"- Process Name: {proc.name()}")
                        print(f"- PID: {proc.pid}")
                        print(f"- CPU Usage: {cpu_usage:.1f}%")
                        print(f"- Memory Usage: {proc.memory_percent():.1f}%")
                        cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else 'N/A'
                        print(f"- Command Line: {cmdline}")
                        parent = proc.parent()
                        parent_info = f"{parent.name()} (PID: {parent.pid})" if parent else 'N/A'
                        print(f"- Parent Process: {parent_info}")
                        print("- Suspicious Connections:")
                        for ip, domain, domain_type in suspicious_connections:
                            print(f"  - {ip} ({domain_type}: {domain})")
                        print()  # Empty line for readability
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
except KeyboardInterrupt:
    print("Monitoring stopped.")