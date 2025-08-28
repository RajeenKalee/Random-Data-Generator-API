## Random Data Generator By Rajeen Kaleerathan  ##

## Imported Libraries ##
import json
import random
from faker import Faker
from faker_music import MusicProvider
from colorama import Fore, Style, init
import re  # Needed to clean country codes

init()
###########################################

fake = Faker()  # Faker instance that generates types of fake data
import faker_music
fake.add_provider(MusicProvider)

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
    locale, code = get_random_locale()
    localized_fake = Faker(locale)
    address = localized_fake.address().replace("\n", ", ")
    return {
        "Address": address,
        "Country Code": code
    }

## Define generator functions mapped by standard data types ##
available_data_types = {
    "full_name": lambda: fake.name(),
    "email_address": lambda: fake.email(),
    "phone_number": generate_global_phone_string,
    "phone_number_int": generate_global_phone_integer,
    "full_address": lambda: fake.address().replace("\n", ", "),
    "alpha2": lambda: get_random_locale()[1],    ## alpha2 looks at the ISO 3166-1 alpha-2 country code format. It’s a two letter country code used show the countries. ##
    "id_number": lambda: random.randint(1000, 999999),
    "boolean": lambda: random.choice([True, False]),
    "date_iso": lambda: fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
    ### Music Data fields ###
    "music_genre": lambda: fake.music_genre(),
    "music_instrument": lambda: fake.music_instrument(),
    "artist_name": lambda: fake.name(),  # Fake artist name
    "song_title": lambda: fake.sentence(nb_words=3).replace(".", ""),  # Remove period
    "album_title": lambda: fake.catch_phrase()
}

## User-friendly field options to display in CLI ##
available_field_types = {
    "Full Name": "full_name",
    "Email": "email_address",
    "Phone Number": "phone_number",
    "Phone Number (Int)": "phone_number_int",
    "Date of Birth": "date_iso",
    "ID Number": "id_number",
    "Is Active": "boolean",
    "Is Employee": "boolean",
    "Address": "full_address",
    "Country Code": "alpha2",   ## alpha2 looks at the ISO 3166-1 alpha-2 country code format. It’s a two letter country code used show the countries. ##
    "Music Genre": "music_genre",
    "Music Instrument": "music_instrument",
    "Artist Name": "artist_name",
    "Song Title": "song_title",
    "Album Title": "album_title"

}

## Display all available field options to the user ##
def display_field_options():
    print()
    print(Fore.LIGHTGREEN_EX + "Available Data Fields:" + Style.RESET_ALL)
    for i, field in enumerate(available_field_types.keys(), 1):
        print(f"{i}. {field}")
    print()

## User selects both output field name and data type ##
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
                display_name = list(available_field_types.keys())[index - 1]
                data_type = available_field_types[display_name]

                ## Prompt user for custom field name (optional) ##
                custom_name = input(f"Enter output field name for '{display_name}' (or press enter to keep as '{display_name}'): ").strip()
                output_field_name = custom_name if custom_name else display_name

                selected_generators[output_field_name] = data_type

            if selected_generators:
                return selected_generators  ## Dict of Output Field Name → Data Type String ##
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

## Generate fake data using field-to-datatype mappings ##
def generate_data(fields, count):
    result = []

    for _ in range(count):
        obj = {}

        for field, dtype in fields.items():
            generator_func = available_data_types.get(dtype)
            if generator_func:
                obj[field] = generator_func()
            else:
                obj[field] = f"[Invalid: {dtype}]"

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