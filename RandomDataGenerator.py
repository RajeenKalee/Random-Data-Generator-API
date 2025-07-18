## Random Data Generator By Rajeen Kaleerathan  ##

## Imported Libraries ##
import json
import random
from faker import Faker
from colorama import Fore, Style, init
import re  ## Needed to clean country codes
init()
###########################################

fake = Faker()  ## Faker instance that generates types of fake data ##

## Stores the current record’s locale so Address and Country Code match ##
def get_random_locale():
    return random.choice([
        ('en_US', 'US'),
        ('en_GB', 'GB'),
        ('fr_FR', 'FR'),
        ('de_DE', 'DE'),
        ('en_CA', 'CA'),
    ])

## Function to return realistic international phone number as a formatted string ##
def generate_global_phone_string():
    country_code = fake.country_calling_code()
    number = fake.msisdn()[3:13]
    return f"({country_code}) {number[:4]} {number[4:]}"


## Function to return international phone number as a numeric-only integer ##
def generate_global_phone_integer():
    raw_code = fake.country_calling_code()
    country_code = re.sub(r"\D", "", raw_code)  # Remove + and spaces
    number = fake.msisdn()[3:13]
    return int(f"{country_code}{number}")


## Function to generate address and matching country code from same locale ##
def generate_address_and_country():
    locale, code = random.choice(supported_locales)  ## Pick a random locale-country pair
    localized_fake = Faker(locale)  ## New faker instance for that locale
    address = localized_fake.address().replace("\n", ", ")  ## Format address for readability
    return {
        "Address": address,
        "Country Code": code
    }


## Available fields mapped to data types and their generator functions ##
available_field_types = {
    "Full Name": {
        "string": lambda: fake.name()  ## Person's full name ##
    },
    "Email": {
        "string": lambda: fake.email()  ## Email address ##
    },
    "Phone Number": {
        "string": generate_global_phone_string,  ## Formatted international phone ##
        "integer": generate_global_phone_integer  ## Raw numeric phone with country code ##
    },
    "Date of Birth": {
        "iso": None  ## Injected at runtime after user inputs age range ##
    },
    "ID Number": {
        "integer": lambda: random.randint(1000, 999999)  ## Simulated unique identifier ##
    },
    "Is Active": {
        "boolean": lambda: random.choice([True, False])  ## Boolean flag: user is active or not ##
    },
    "Is Employee": {
        "boolean": lambda: random.choice([True, False])  ## Boolean flag: If they are a part of the company ##
    },
    "Address": {
        "string": None  ## Will be generated using locale matched Faker instance ##
    },
    "Country Code": {
        "string": None  ## Will match the country for the generated address ##
    }
}



## Function Factory to create Date of Birth generator with custom age range ##
def make_dob_generator_with_prompt():
    while True:
        try:
            min_age = int(input("Enter minimum age for Date of Birth: ").strip())
            max_age = int(input("Enter maximum age for Date of Birth: ").strip())
            if min_age < 0 or max_age < min_age:
                raise ValueError
            return lambda: fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).isoformat()
        except ValueError:
            print(Fore.RED + "Invalid age range. Please enter valid numbers.\n" + Style.RESET_ALL)


## Display all available field options to the user ##
def display_field_options():
    print()
    print(Fore.LIGHTGREEN_EX + "Available Data Fields:" + Style.RESET_ALL)
    for i, field in enumerate(available_field_types.keys(), 1):
        print(f"{i}. {field}")
    print()


## User selects both field and data type for generation ##
def get_user_field_selection():
    selected_generators = {}

    while True:
        display_field_options()
        print(Fore.LIGHTGREEN_EX + "Enter the numbers of the fields you'd like (comma-separated):" + Style.RESET_ALL)
        user_input = input("Your selection: ").strip()

        if not user_input:
            print("No input provided.\n")
            continue

        raw_items = user_input.split(',')
        try:
            for item in raw_items:
                item = item.strip()
                index = int(item)
                if index < 1 or index > len(available_field_types):
                    raise ValueError(f"Invalid option: {index}")
                field_name = list(available_field_types.keys())[index - 1]

                ## Ask for type ##
                type_options = available_field_types[field_name]
                print(f"Available types for '{field_name}':")
                for i, dtype in enumerate(type_options.keys(), 1):
                    print(f"  {i}. {dtype}")
                type_choice = input(f"Choose data type for '{field_name}': ").strip()

                ## Accept either index or name of type ##
                if type_choice.isdigit():
                    type_index = int(type_choice)
                    dtype = list(type_options.keys())[type_index - 1]
                elif type_choice in type_options:
                    dtype = type_choice
                else:
                    raise ValueError("Invalid type choice.")

                ## Handle Date of Birth age prompt separately ##
                if field_name == "Date of Birth" and dtype == "iso":
                    selected_generators[field_name] = make_dob_generator_with_prompt()
                else:
                    selected_generators[field_name] = available_field_types[field_name][dtype]
            if selected_generators:
                return selected_generators  ## Dict of Field → Generator functions ##
            else:
                print(Fore.RED + "No valid fields selected.\n" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"\nInvalid input: {e}\n" + Style.RESET_ALL)


## Ask how many records to generate ##
def get_object_count():
    while True:
        try:
            count = int(input("How many objects would you like to generate? "))
            if count <= 0:
                raise ValueError("Please choose a number greater than 0!")
            return count
        except ValueError:
            print(Fore.RED + "Please enter a valid positive integer.\n" + Style.RESET_ALL)


## Ask user for output format (NDJSON / JSON) using numbered options ##
def get_output_format():
    while True:
        print("\nOutput format:")
        print("1. NDJSON")
        print("2. JSON")
        choice = input("Choose format (1 or 2): ").strip()
        if choice == "1":
            return "ndjson"
        elif choice == "2":
            return "json"
        else:
            print(Fore.RED + "Invalid input. Please choose 1 or 2.\n" + Style.RESET_ALL)


## Generate fake data based on user-defined fields and types ##
def generate_data(fields, count):
    result = []

    for _ in range(count):
        obj = {}

        ## Shared locale for Address and Country Code consistency ##
        locale, country_code = get_random_locale()
        localized_fake = Faker(locale)

        for field, dtype in fields.items():
            ## Special case: Locale-based address ##
            if field == "Address":
                obj[field] = localized_fake.address().replace("\n", ", ")

            ## Special case: Country Code tied to locale ##
            elif field == "Country Code":
                obj[field] = country_code

            ## Standard field → resolve function → call it ##
            elif field in available_field_types and dtype in available_field_types[field]:
                generator_func = available_field_types[field][dtype]
                obj[field] = generator_func()

            ## Invalid field or type ##
            else:
                obj[field] = f"[Invalid: {field} - {dtype}]"

        result.append(obj)

    return result




## Display generated data in chosen format ##
def display_data(data, fmt):
    print()
    print(Fore.LIGHTGREEN_EX + "Generated Data:\n" + Style.RESET_ALL)
    if fmt == "ndjson":
        for item in data:
            print(json.dumps(item))
    else:  ## json
        print(json.dumps(data, indent=2))
    print()


## Main CLI flow for generating random data ##
def main():
    print(Fore.LIGHTRED_EX + "\nRandom Data Generator - By Rajeen K\n" + Style.RESET_ALL)

    while True:
        selected_generators = get_user_field_selection()
        count = get_object_count()
        fmt = get_output_format()
        data = generate_data(selected_generators, count)
        display_data(data, fmt)

        ## Ask if user wants to generate more data ##
        again = input("\nDo you want to generate more data? (y/n): ").strip().lower()
        if again != "y":
            print(Fore.LIGHTGREEN_EX + "\nThank you for using the generator!\n" + Style.RESET_ALL)
            break


if __name__ == "__main__":  ## Runs the main() function only if this script is run directly ##
    main()
