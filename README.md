# Random Data Generator API

A Python-based project that allows you to define schemas and generate fake data using Faker. Includes both a command-line tool and a Flask API.

## Features

- Create and store data schemas
- Generate random user data (ID, name, address, etc.)
- Expose data generation via REST API

## Usage

### CLI:
Run `RandomDataGenerator.py` and follow prompts to create and manage schemas.

### API:
- `GET /` – Test message
- `GET /schemas` – List all saved schemas
- `GET /schemas/<name>/data` – Generate data from a named schema
