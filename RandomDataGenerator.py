## Random Data Generator By Rajeen Kaleerathan ##

## Imported Libraries ##
import json
import random
from faker import Faker
from colorama import Fore, Style, init
init()
###########################################


def main():
    while True:
        print("")
        print(Fore.LIGHTRED_EX + "Random Data Generator - By Rajeen K"  + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX + "Please select from the options below" + Style.RESET_ALL)
        print("")
        print("1. Create New Schema")
        print("2. List Schemas")
        print("3. Run a Schema")
        print("4. Delete a Schema")
        print("")
        print("5. Exit")
        print("")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_new_schema()
        elif choice == "2":
            list_schemas()
        elif choice == "3":
            name = input("Enter the schema name to run: ").strip()
            run_schema(name)
        elif choice == "4":
            name = input("Enter the schema name to delete: ").strip()
            delete_schema(name)
        elif choice == "5":
            print("\nThank you!\n")
            break
        else:
            print("Invalid choice. Please select a number from the menu.")


fake = Faker() ## Faker instance that generates types of fake data ##
SCHEMA_FILE = "schemas.json"

data_fields = {
    "ID Number": lambda: random.randint(1, 99999), ## Each value here is a lambda function that returns a randomly generated piece of data for that field. ##
    "Username": lambda: fake.user_name(),
    "Full Name": lambda: fake.name(),
    "DOB (DD/MM/YYYY)": lambda: fake.date_of_birth().strftime("%d/%m/%Y"), ## Date set for UK Region ##
    "Email": lambda: fake.email(),
    "Phone Number": lambda: fake.phone_number(),
    "Address": lambda: fake.address(),
    "IPv4 Address": lambda: fake.ipv4(),
}


def save_schema(name, fields, count):
    schema = load_schemas()
    schema[name] = {"fields": fields, "count": count}
    with open(SCHEMA_FILE, "w") as f:
        json.dump(schema, f, indent=2)


def load_schemas():
    try:
        with open(SCHEMA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def delete_schema(name):
    schema = load_schemas()
    if name in schema:
        del schema[name]
        with open(SCHEMA_FILE, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"Schema '{name}' deleted.")
    else:
        print(f"No schema found with name '{name}'.")


def list_schemas():
    schemas = load_schemas()
    if not schemas:
        print("No schemas available.\n")
    else:
        print(Fore.LIGHTGREEN_EX + "\nAvailable Schemas:" + Style.RESET_ALL)
        for name, schema in schemas.items():
            print(f"• {name} ----- Fields: {schema['fields']}, Count: {schema['count']}")
        print()


def generate_data(fields, count):
    result = []
    for _ in range(count):
        obj = {field: data_fields[field]() for field in fields} ## Generates a fake data record using the selected fields ##
        result.append(obj)
    return result


def display_field_options():
    print()
    print(Fore.LIGHTGREEN_EX + "Please pick from the list of data fields you would like to generate:" + Style.RESET_ALL)
    print()
    for i, field in enumerate(data_fields.keys(), 1): ## Displays the field options to the user from the list of fields above ##
        print(f"{i}. {field}")
    print()


def get_user_field_selection():
    while True:
        display_field_options()  ## Displays the field options again when creating a schema ##
        print(Fore.LIGHTGREEN_EX + "Enter the numbers of the fields you'd like! (Please separate them with commas!):" + Style.RESET_ALL)
        user_input = input("Your selection: ").strip() ## Collects the users input on field selection ##

        if not user_input:
            print("No input provided.\n") ## Validation is done here if nothing has been entered in ##
            continue

        raw_items = user_input.split(',')
        indices = []

        try:
            for item in raw_items:
                item = item.strip()
                index = int(item)  ## Throws an error if it's not an integer ##
                if index < 1 or index > len(data_fields): ## Validation is done here if number entered is not part of the list ##
                    raise ValueError(f"Option {index} is not an option!.")
                indices.append(index)

            selected_fields = [list(data_fields.keys())[i - 1] for i in indices] ## Get selected field names based on user chosen numbers ##
            return selected_fields

        except ValueError:
            print(Fore.RED + "\nInvalid input. Please input numbers from the list of options!.\n" + Style.RESET_ALL)


def get_object_count():
    while True:
        try:
            count = int(input("How many objects would you like to generate? ")) ## Asks user how many object
            if count <= 0:  ## Validation is done here if number entered is 0 or below ##
                raise ValueError("Please choose a number greater than 0!")
            return count
        except ValueError:
            print(Fore.RED + "Please enter a valid positive integer.\n" + Style.RESET_ALL)


def display_data_ndjson(data):
    print("")
    print("")
    for item in data:
        print(json.dumps(item)) ## Puts the dictionary to a NDJSON formatted string and prints to the response body ##
    print("")
    print("")



def run_schema(name):
    schemas = load_schemas()
    if name not in schemas:
        print(f"No schema named '{name}'.")
        return
    schema = schemas[name]
    data = generate_data(schema["fields"], schema["count"])
    display_data_ndjson(data)  ## This will Print it to the response body ##



def create_new_schema():
    selected_fields = get_user_field_selection() ## Grabs the user field selection ##
    count = get_object_count() ## Counts how many objects to generate from the user input ##
    name = input("Enter a name for your schema: ").strip()
    save_schema(name, selected_fields, count)
    print(Fore.LIGHTGREEN_EX + f"Schema '{name}' created.\n" + Style.RESET_ALL)


if __name__ == "__main__": ## Runs the main() function only if this script is run directly ##
    main()
