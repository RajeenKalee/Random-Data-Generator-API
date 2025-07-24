import pytest
from RandomDataGenerator import (
    generate_global_phone_string,
    generate_global_phone_integer,
    generate_address_and_country,
    generate_data,
    available_data_types
)

## Test string based phone number format ##
def test_phone_string_returns_string():
    phone = generate_global_phone_string()
    assert isinstance(phone, str)
    assert "(" in phone and ")" in phone

## Test integer based phone number format ##
def test_phone_integer_returns_integer():
    phone = generate_global_phone_integer()
    assert isinstance(phone, int)
    assert len(str(phone)) >= 10

## Test that address and country code return a proper structure ##
def test_address_and_country_structure():
    result = generate_address_and_country()
    assert isinstance(result, dict)
    assert "Address" in result
    assert "Country Code" in result

## Test data generation for full_name type ##
def test_generate_single_name():
    fields = {"Full Name": "full_name"}  ## Schema format: label → data_type ##
    data = generate_data(fields, 1)
    assert len(data) == 1
    assert "Full Name" in data[0]
    assert isinstance(data[0]["Full Name"], str)

## Test data generation for email_address type ##
def test_generate_email_field():
    fields = {"Email": "email_address"}  ## Schema format: label → data_type ##
    data = generate_data(fields, 1)
    assert "@" in data[0]["Email"]
