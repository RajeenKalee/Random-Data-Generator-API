# Random Data Generator API - Testing the GitHub Webhook

A Python based application for generating realistic fake data based on user defined schemas. It includes a command-line interface and a RESTful Flask API for defining, storing, and executing data schemas. Useful for prototyping, testing, and populating mock datasets.

## Overview

The application allows you to:
- Define flexible data schemas where field names are arbitrary and the values indicate the type of data to generate
- Generate structured random data using the Faker library
- Access functionality either via the command line or over a REST API
- Output data in JSON or NDJSON formats

## Features

- Schema-based data generation
- Support for multiple data types (names, emails, phone numbers, addresses, etc.)
- Locale-aware address and country code generation
- RESTful API for schema management and data access
- CLI for interactive data creation
- Unit and integration test coverage

## Supported Data Types

Schema values must be one of the supported data types:
- `full_name`
- `email_address`
- `phone_number` (string format)
- `phone_number_int` (numeric-only format)
- `full_address`
- `alpha2` (ISO 2-letter country code)
- `boolean`
- `id_number`
- `date_iso` (date of birth in ISO 8601 format)



## Example Schema Format ##

```json
{
  "CustomerName": "full_name",
  "Email": "email_address",
  "Phone": "phone_number",
  "Country": "alpha2",
  "IsSubscribed": "boolean"
}