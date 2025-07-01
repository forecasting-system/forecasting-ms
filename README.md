# Forecasting Microservice

## Overview

This is a forecasting microservice that uses machine learning models to predict future values based on historical data.

## Technical decisions

- It keeps separated the message broker for events and the message broker for messaging. This is because events are, among others, used for external communication, it could be necessary to have a different message broker for this purpose while keeping the internal communication within the same message broker.

## Setup

### Installation

```
poetry install
```

### Startup

```
poetry run uvicorn app.entrypoints.main:app --reload
```

OR

```
poetry run poe start
```

### Test it isolated

```
docker run --rm -it --network host synadia/nats-box

nats pub internal.sales.persisted "test message"

nats sub internal.forecast.generated

```
