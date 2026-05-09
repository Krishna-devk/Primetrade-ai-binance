# Binance Futures Testnet Trading Bot

## Project Intuition

This project is a **production-inspired CLI trading utility** built for Binance Futures Testnet (USDT-M).

The goal of the assignment is **not** to build a hedge fund engine or a complete trading platform.

The real objective is to demonstrate:

* Clean software engineering
* API integration skills
* Validation and defensive programming
* Structured logging
* Operational reliability
* Maintainable architecture
* CLI developer experience

This project is intentionally designed as a **small but polished operational tool**.

The philosophy of this architecture is:

> Build the smallest possible system that still feels production-aware.

---

# Core Engineering Principles

This project demonstrates:

| Principle               | Implementation                  |
| ----------------------- | ------------------------------- |
| Separation of Concerns  | Modular layered architecture    |
| Reliability Engineering | Validation + graceful failures  |
| Operational Readiness   | Health check commands           |
| Observability           | Structured logging              |
| Security Awareness      | `.env` + `.gitignore`           |
| UX Consistency          | Rich CLI formatting             |
| Maintainability         | Typed models + reusable modules |

---

# Final Project Architecture

## High-Level Workflow

```text
                USER
                  │
                  ▼
         ┌─────────────────┐
         │   cli.py        │
         │ Typer Commands  │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ validators.py   │
         │ Input Validation│
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  models.py      │
         │ Typed Contracts │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  orders.py      │
         │ Business Logic  │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  client.py      │
         │ Binance Wrapper │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────────────┐
         │ Binance Futures Testnet │
         └─────────────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ display.py      │
         │ Rich UI Output  │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ logs/           │
         │ Structured Logs │
         └─────────────────┘
```

---

# Final Folder Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── display.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── models.py
│   ├── orders.py
│   └── validators.py
│
├── logs/
│   └── trading_bot.log
│
├── cli.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

---

# Responsibility of Each File

| File                | Responsibility                  |
| ------------------- | ------------------------------- |
| `cli.py`            | CLI entry point + orchestration |
| `client.py`         | Binance API communication       |
| `orders.py`         | Business logic layer            |
| `validators.py`     | Input validation                |
| `models.py`         | Typed dataclasses               |
| `display.py`        | Rich terminal UI                |
| `exceptions.py`     | Human-readable error mapping    |
| `config.py`         | Environment variable management |
| `logging_config.py` | Logging setup/configuration     |

---

# Technology Stack

| Purpose               | Tool                  |
| --------------------- | --------------------- |
| CLI                   | Typer                 |
| Terminal UI           | Rich                  |
| Binance Integration   | python-binance        |
| Environment Variables | python-dotenv         |
| Logging               | Python logging module |

---

# Why FastAPI Was NOT Used

This project intentionally avoids FastAPI because:

* The assignment specifically requests a CLI application
* Adding HTTP/API infrastructure increases unnecessary complexity
* A CLI utility is more aligned with the assignment requirements
* Simpler architecture improves reliability and maintainability

This demonstrates:

> Correct tool selection for the scope of the problem.

---

# Step-by-Step Execution Plan

# STEP 1 — Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

## Windows

```bash
venv\Scripts\activate
```

## Linux / Mac

```bash
source venv/bin/activate
```

---

# STEP 2 — Install Dependencies

```bash
pip install python-binance==1.0.19 typer[all]==0.9.0 rich==13.7.0 python-dotenv==1.0.0
```

Optional formatting tools:

```bash
pip install black isort
```

Freeze dependencies:

```bash
pip freeze > requirements.txt
```

---

# STEP 3 — Create `.gitignore`

```gitignore
.env
logs/
venv/
__pycache__/
*.pyc
```

---

# STEP 4 — Setup Binance Futures Testnet

Go to:

https://testnet.binancefuture.com

Generate:

* API Key
* Secret Key

Create `.env`

```env
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

---

# STEP 5 — Build `config.py`

## Responsibilities

* Load `.env`
* Validate credentials
* Fail gracefully if missing

## Required Fixes

* If `.env` missing → show readable error
* If API keys empty → raise ConfigError

---

# STEP 6 — Build `logging_config.py`

## Responsibilities

* Create logs directory
* Configure structured logger
* Enable operational observability

## Important Fix

```python
os.makedirs("logs", exist_ok=True)
```

## Log Format

```text
2026-05-09 18:10:01 | INFO | MARKET BUY BTCUSDT qty=0.01
```

## Log Levels

| Event              | Level    |
| ------------------ | -------- |
| Validation         | INFO     |
| Request Sent       | INFO     |
| Validation Failure | WARNING  |
| API Failure        | ERROR    |
| Unexpected Crash   | CRITICAL |

## Never Log

* API secret
* Authorization headers
* Sensitive credentials

---

# STEP 7 — Build `models.py`

Use immutable dataclasses.

## Models

* `OrderRequest`
* `OrderResponse`

## Example Design

```python
@dataclass(frozen=True)
```

This improves:

* maintainability
* type safety
* predictability

---

# STEP 8 — Build `validators.py`

## Responsibilities

Validate:

* symbol
* side
* order type
* quantity
* price
* notional value
* maximum quantity

---

# Validation Rules

| Rule           | Condition                      |
| -------------- | ------------------------------ |
| Symbol         | uppercase + endswith("USDT")   |
| Side           | BUY or SELL                    |
| Type           | MARKET or LIMIT                |
| Quantity       | > 0                            |
| Price          | required for LIMIT             |
| Price          | > 0                            |
| Notional Value | > 10 USDT                      |
| Quantity Limit | prevent huge accidental orders |

---

# Precision Strategy

Use:

```python
from decimal import Decimal
```

Avoid raw float math.

Round:

* quantity → 3 decimals
* price → 2 decimals

---

# STEP 9 — Build `exceptions.py`

Create centralized Binance error mapping.

## Example

```python
ERROR_MAP = {
    -2014: "Invalid API credentials.",
    -2019: "Insufficient futures margin.",
    -1121: "Invalid trading symbol.",
    -1021: "System clock out of sync."
}
```

This creates:

* cleaner UX
* readable failures
* operational clarity

---

# STEP 10 — Build `client.py`

## Responsibilities

ONLY:

* initialize Binance client
* communicate with Binance
* fetch account data
* place orders

---

# Important Futures Testnet Fix

```python
client = Client(api_key, api_secret, testnet=True)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
```

---

# Methods to Implement

| Method           | Purpose              |
| ---------------- | -------------------- |
| `ping()`         | connectivity check   |
| `get_balance()`  | account verification |
| `get_price()`    | market info          |
| `create_order()` | order placement      |

---

# Required Exception Handling

Handle:

* API failures
* network failures
* timeouts
* invalid credentials

Also handle:

```python
requests.exceptions.Timeout
requests.exceptions.ConnectionError
```

---

# STEP 11 — Build `orders.py`

This is the business logic layer.

## Responsibilities

* Prepare payloads
* Convert decimals safely
* Add timeInForce
* Measure execution time
* Log operations
* Return typed responses

---

# Critical LIMIT Order Fix

Always use:

```python
timeInForce="GTC"
```

---

# Float Safety

Convert:

* quantity
* price

to strings before sending to Binance.

Example:

```python
str(quantity)
```

---

# STEP 12 — Build `display.py`

## Responsibilities

* Rich tables
* Success banners
* Error banners
* Health check display
* Order summaries

---

# Final Color Language

| Event     | Style       |
| --------- | ----------- |
| INFO      | Cyan        |
| VALIDATED | Blue        |
| SUCCESS   | Bold Green  |
| WARNING   | Bold Yellow |
| ERROR     | Bold Red    |

---

# Special LIMIT Order UX

If order status is `NEW`:

```text
This limit order remains open until market price reaches your specified value.
```

This prevents reviewer confusion.

---

# STEP 13 — Build `cli.py`

Use Typer subcommands.

## Commands

| Command | Purpose            |
| ------- | ------------------ |
| `check` | health check       |
| `place` | place order        |
| `info`  | market information |

---

# Example Commands

## Health Check

```bash
python cli.py check
```

---

## MARKET Order

```bash
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

---

## LIMIT Order

```bash
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
```

---

## Market Info

```bash
python cli.py info --symbol BTCUSDT
```

---

# STEP 14 — Global Exception Handling

At CLI entrypoint:

Handle:

* KeyboardInterrupt
* unexpected failures

Never expose raw tracebacks to terminal users.

Instead:

* show concise error
* log full traceback internally

---

# STEP 15 — Generate Logs

Run:

1. One MARKET order
2. One LIMIT order

Ensure logs are:

* clean
* readable
* chronological

---

# STEP 16 — README Sections

Your README should contain:

```md
# Binance Futures Testnet Trading Bot

## Overview
## Features
## Architecture
## Project Structure
## Installation
## Environment Variables
## Quick Start
## Commands
## Validation Rules
## Logging
## Error Handling
## Assumptions & Constraints
## Troubleshooting
## Future Improvements
```

---

# Assumptions & Constraints

## Time Sync

Assumes system clock is synchronized via NTP.

## Precision

Uses:

* quantity rounding → 3 decimals
* price rounding → 2 decimals

In production:

* precision should be fetched dynamically from `exchangeInfo`.

## Environment

Requires:

* Python 3.10+
* valid Binance Futures Testnet API keys

---

# Troubleshooting

## Timestamp Error

If you encounter:

```text
-1021 Timestamp outside recvWindow
```

Sync your system clock.

---

## Futures Permission Error

Ensure:

* Binance Futures Testnet API permissions are enabled.

---

# Future Improvements

```md
- Dynamic precision parsing from exchangeInfo
- Retry/backoff mechanisms
- WebSocket market monitoring
- Stop-Limit orders
- Automated unit tests
```

---

# STEP 17 — Format Code

Run:

```bash
black .
isort .
```

---

# STEP 18 — Final Testing

Create fresh environment and test:

```bash
pip install -r requirements.txt
python cli.py check
```

Then:

* MARKET order
* LIMIT order

Verify:

* logs
* output
* README commands

---

# STEP 19 — Final GitHub Checklist

Before submission:

* [ ] `.env` excluded
* [ ] no secrets committed
* [ ] logs sanitized
* [ ] README accurate
* [ ] requirements pinned
* [ ] no debug code
* [ ] no unused files
* [ ] clean project structure

---

# Final Engineering Mindset

This project is NOT about advanced trading logic.

It is about demonstrating:

* disciplined execution
* operational reliability
* maintainable architecture
* defensive programming
* professional developer tooling

The goal is to make the reviewer think:

> “This person can contribute safely to a real engineering codebase.”

That is the real success condition of this assignment.
