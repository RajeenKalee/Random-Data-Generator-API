import pytest
from RandomDataGenerator import (
    generate_global_phone_string,
    generate_global_phone_integer,
    generate_address_and_country,
    generate_data,
    available_field_types
)

def test_phone_string_returns_string():
    phone = generate_global_phone_string()
    assert isinstance(phone, str)
    assert "(" in phone and ")" in phone

def test_phone_integer_returns_integer():
    phone = generate_global_phone_integer()
    assert isinstance(phone, int)
    assert len(str(phone)) >= 10

def test_address_and_country_structure():
    result = generate_address_and_country()
    assert isinstance(result, dict)
    assert "Address" in result
    assert "Country Code" in result

def test_generate_single_name():
    fields = {"Full Name": available_field_types["Full Name"]["string"]}
    data = generate_data(fields, 1)
    assert len(data) == 1
    assert "Full Name" in data[0]

def test_generate_email_field():
    fields = {"Email": "string"}
    data = generate_data(fields, 1)
    assert "@" in data[0]["Email"]

