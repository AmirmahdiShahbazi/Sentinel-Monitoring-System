# 🛡️ Sentinel: Async Plugin-Based Monitor

Sentinel is a high-performance, asynchronous monitoring engine built with Python. It allows you to track website availability and system hardware health in real-time through a beautiful, live-updating terminal dashboard.

Designed with **SOLID principles**, Sentinel is fully modular. You can add new types of checks or notification alerts without ever touching the core engine.

---

## ✨ Features

* **⚡ Fully Asynchronous:** Powered by `asyncio` and `httpx`. Performs hundreds of checks concurrently without blocking.
* **📊 Live Dashboard:** A sleek, real-time terminal UI built with `Rich`.
* **🔌 Plugin Architecture:** Easy to extend using Strategy and Observer patterns.
* **⚙️ JSON Configured:** No hard-coding. Manage your targets and thresholds via `config.json`.
* **🛡️ Resource Efficient:** Low overhead monitoring for CPU and RAM usage.

---

## 🛠️ Architecture (Design Patterns)

This project was built to demonstrate clean, scalable Python architecture:

1.  **Strategy Pattern**: Every "Check" (HTTP, System) implements a common interface, making them interchangeable.
2.  **Observer Pattern**: The Engine notifies a list of "Alerts" (Console, Log) whenever a check fails.
3.  **Factory Pattern**: A central factory instantiates objects dynamically based on the JSON configuration.
4.  **Separation of Concerns**: UI (Dashboard), Logic (Engine), and Data (Config) are strictly decoupled.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.8+
* pip (Python package manager)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/sentinel.git](https://github.com/yourusername/sentinel.git)
cd sentinel

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# 🛡️ Sentinel: Async Plugin-Based Monitor

Sentinel is a high-performance, asynchronous monitoring engine built with Python. It allows you to track website availability and system hardware health in real-time through a beautiful, live-updating terminal dashboard.

Designed with **SOLID principles**, Sentinel is fully modular. You can add new types of checks or notification alerts without ever touching the core engine.

---

## ✨ Features

* **⚡ Fully Asynchronous:** Powered by `asyncio` and `httpx`. Performs hundreds of checks concurrently without blocking.
* **📊 Live Dashboard:** A sleek, real-time terminal UI built with `Rich`.
* **🔌 Plugin Architecture:** Easy to extend using Strategy and Observer patterns.
* **⚙️ JSON Configured:** No hard-coding. Manage your targets and thresholds via `config.json`.
* **🛡️ Resource Efficient:** Low overhead monitoring for CPU and RAM usage.

---

## 🛠️ Architecture (Design Patterns)

This project was built to demonstrate clean, scalable Python architecture:

1.  **Strategy Pattern**: Every "Check" (HTTP, System) implements a common interface, making them interchangeable.
2.  **Observer Pattern**: The Engine notifies a list of "Alerts" (Console, Log) whenever a check fails.
3.  **Factory Pattern**: A central factory instantiates objects dynamically based on the JSON configuration.
4.  **Separation of Concerns**: UI (Dashboard), Logic (Engine), and Data (Config) are strictly decoupled.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.8+
* pip (Python package manager)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/sentinel.git](https://github.com/yourusername/sentinel.git)
cd sentinel

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

### 4. Usage

Run the entry point script to start the monitoring engine and launch the live terminal dashboard:

```bash
python main.py

## 📂 Project Structure

The project is organized to maintain a strict separation between the core engine and the extensible plugin system:

* **`core/`**: The brain of the application.
    * `base.py`: Abstract base classes (interfaces) for Checks and Alerts.
    * `engine.py`: The asynchronous loop that orchestrates check execution.
    * `factory.py`: Handles dynamic object creation from JSON configuration.
    * `dashboard.py`: Encapsulates all `Rich` UI and table rendering logic.
* **`plugins/`**: Individual monitoring and notification modules.
    * `checks/`: Contains `http_check.py` and `system_check.py`.
    * `alerts/`: Contains `console_alert.py` and `log_alert.py`.
* **`config.json`**: The central configuration file for setting intervals and targets.
* **`main.py`**: The entry point that initializes the engine and starts the live display.
* **`requirements.txt`**: Lists all external dependencies (`httpx`, `psutil`, `rich`).
* **`.gitignore`**: Prevents logs and environment files from being tracked by Git.

---