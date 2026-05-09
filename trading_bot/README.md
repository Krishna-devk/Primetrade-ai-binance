# Binance Futures Testnet Trading Bot

## Overview

This is a production-inspired CLI trading utility built for Binance Futures Testnet (USDT-M). The goal is to demonstrate clean software engineering, API integration skills, validation, structured logging, and maintainable architecture.

## Features

- Health check command
- Place MARKET and LIMIT orders
- Market information retrieval
- Input validation and error handling
- Structured logging
- Rich terminal UI

## Architecture

The project follows a modular layered architecture with separation of concerns:

- `cli.py`: CLI entry point and orchestration
- `bot/client.py`: Binance API communication
- `bot/orders.py`: Business logic layer
- `bot/validators.py`: Input validation
- `bot/models.py`: Typed dataclasses
- `bot/display.py`: Rich terminal UI
- `bot/exceptions.py`: Error mapping
- `bot/config.py`: Environment variable management
- `bot/logging_config.py`: Logging setup

## Project Structure

```
trading_bot/
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
├── logs/
│   └── trading_bot.log
├── cli.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the `trading_bot` directory with your Binance Futures Testnet API credentials:

```
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

Get your API keys from [Binance Futures Testnet](https://testnet.binancefuture.com).

## Quick Start

1. Activate the virtual environment
2. Run health check:
   ```bash
   python cli.py check
   ```
3. Place a MARKET order:
   ```bash
   python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
   ```
4. Place a LIMIT order:
   ```bash
   python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
   ```
5. Get market info:
   ```bash
   python cli.py info --symbol BTCUSDT
   ```

## Commands

- `check`: Perform health check (connectivity and balance)
- `place`: Place an order (MARKET or LIMIT)
- `info`: Get current market price for a symbol

## Validation Rules

- Symbol: Must be uppercase and end with "USDT"
- Side: BUY or SELL
- Type: MARKET or LIMIT
- Quantity: > 0, rounded to 3 decimals, max 100
- Price: Required for LIMIT orders, > 0, rounded to 2 decimals
- Notional value: >= 10 USDT for LIMIT orders

## Logging

Logs are stored in `logs/trading_bot.log` with the format:
```
2026-05-09 18:10:01 | INFO | MARKET BUY BTCUSDT qty=0.01
```

## Error Handling

- API errors are mapped to human-readable messages
- Validation errors are shown clearly
- Network errors are handled gracefully
- Unexpected errors log full tracebacks internally

## Assumptions & Constraints

- System clock is synchronized via NTP
- Uses fixed precision (quantity: 3 decimals, price: 2 decimals)
- Requires Python 3.10+ and valid Binance Futures Testnet API keys

## Troubleshooting

- **Timestamp error (-1021)**: Sync your system clock
- **Futures permission error**: Ensure Binance Futures Testnet API permissions are enabled
- **Connectivity issues**: Check internet connection and API keys

## Future Improvements

- Dynamic precision parsing from exchangeInfo
- Retry/backoff mechanisms
- WebSocket market monitoring
- Stop-Limit orders
- Automated unit tests