# MineDetector

MineDetector is an open-source tool designed to detect unauthorized cryptocurrency mining (cryptojacking) on your system. It monitors CPU usage and network connections to identify processes that may be engaging in mining activities without your consent. By checking for connections to known mining pools—both cryptojacking-related and legitimate—MineDetector helps you safeguard your system's resources.

## Key Features

*   **CPU Monitoring:** Tracks processes with high CPU usage (above a configurable threshold).
*   **Network Connection Analysis:** Checks if high-CPU processes are connected to known mining pool domains.
*   **Reporting:** Provides comprehensive information about suspicious processes, including process name, PID, CPU and memory usage, command line, parent process, and connection details.
*   **Cross-Platform:** Works on Windows, macOS, and Linux.
*   **Configurable:** Easily update domain lists, adjust CPU thresholds, and modify monitoring intervals.

## Table of Contents

*   [Installation](#installation)
*   [Usage](#usage)
*   [Configuration](#configuration)
*   [How It Works](#how-it-works)
*   [Limitations](#limitations)
*   [Contributing](#contributing)
*   [License](#license)

## Installation

### Prerequisites

*   **Python 3.x:** Ensure Python 3 is installed on your system. You can check this by running:
    
    ```
    python --version
    ```
    
    or
    
    ```
    python3 --version
    ```
    
*   **psutil Library:** Install the psutil library, which is used for system monitoring:
    
    ```
    pip install psutil
    ```
    
    or
    
    ```
    pip3 install psutil
    ```
    

### Setup

1.  Clone or download the project repository from GitHub.
2.  Navigate to the project directory:
    
    ```
    cd minedetector
    ```
    
3.  Ensure the `minedetector.py` script is in the project directory.

## Usage

### Running the Script

1.  Open a terminal or command prompt.
2.  Execute the script using Python:
    
    ```
    python minedetector.py
    ```
    
    or
    
    ```
    python3 minedetector.py
    ```
    
3.  The tool will continuously monitor your system and print detailed information about any suspicious processes detected.
4.  To stop the monitoring, press `Ctrl+C`.

### Example Output

2023-10-05 14:30:00 Suspicious process detected:
- Process Name: chrome.exe
- PID: 1234
- CPU Usage: 85.0%
- Memory Usage: 12.5%
- Command Line: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --type=renderer
- Parent Process: chrome.exe (PID: 5678)
- Suspicious Connections:
  - 192.168.1.100 (Cryptojacking Domain: coinhive.com)
  - 10.0.0.1 (Legitimate Mining Pool: antpool.com)
  

## Configuration

You can customize the behavior of MineDetector by modifying the following parameters in the `minedetector.py` script:

### 1\. Mining Pool Domain Lists

*   **Cryptojacking Domains:** A list of domains associated with cryptojacking activities.
*   **Legitimate Mining Pools:** A list of known legitimate mining pool domains.
*   **Update:** Add or remove domains as needed to keep the lists current.

### 2\. CPU Usage Threshold

*   **Default:** 70%
*   **Modify:** Change the value in the line `if cpu_usage > 70` to set a different threshold for high CPU usage.

### 3\. Monitoring Interval

*   **Default:** 10 seconds
*   **Modify:** Adjust the `time.sleep(10)` value to change how frequently the system is checked.

## How It Works

MineDetector operates by performing the following steps:

### Domain Resolution

The tool resolves the provided lists of mining pool domains (both cryptojacking and legitimate) into IP addresses using `socket.getaddrinfo`. This includes both IPv4 and IPv6 addresses.

### CPU Monitoring

It establishes a baseline for CPU usage measurement using psutil. Every 10 seconds, it checks all running processes for CPU usage above the configured threshold (default: 70%).

### Network Connection Checks

For processes exceeding the CPU threshold, the tool examines their network connections. If a connection is made to an IP address associated with a known mining pool, the process is flagged as suspicious.

### Detailed Reporting

When a suspicious process is detected, the tool outputs a detailed report, including:

*   Timestamp of detection
*   Process name and PID
*   CPU and memory usage
*   Command line arguments
*   Parent process information
*   IP addresses and domain types (cryptojacking or legitimate mining pool)

This approach ensures that users receive comprehensive and actionable information about potential mining activities on their systems.

## Limitations

*   **Static Domain Lists:** The tool relies on predefined lists of mining pool domains. These lists may become outdated, requiring periodic updates.
*   **False Positives:** Legitimate processes (e.g., web browsers) may connect to domains that are also used by mining pools, leading to false positives.
*   **Detection Only:** MineDetector detects suspicious activity but does not take action to stop or remove the processes. Users must manually intervene.
*   **Advanced Evasion Techniques:** Sophisticated mining malware may use proxies or other methods to hide their connections, potentially evading detection.

## Contributing

We welcome contributions to improve MineDetector! Here’s how you can help:

*   **Code Contributions:** Submit pull requests with enhancements, bug fixes, or new features.
*   **Issue Reporting:** Open issues on GitHub to report bugs or suggest improvements.
*   **Domain List Updates:** Help keep the mining pool domain lists current by submitting updates.

Please follow the Contributing Guidelines (see `CONTRIBUTING.md`) when submitting contributions.

## License

This project is licensed under the MIT License (see `LICENSE`). You are free to use, modify, and distribute this software in accordance with the terms of the license.