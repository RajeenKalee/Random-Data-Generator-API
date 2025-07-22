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
        display_field_options() ## Displays the Data Field options ##
        selected_fields = get_user_field_selection() ## Grabs the user field selection ##
        count = get_object_count() ## Counts how many objects to generate from the user input ##
        generated_data = generate_data(selected_fields, count) ## Generates the data from Faker ##
        export_to_ndjson(generated_data) ## Exports the file to the NDJSON format ##

        ## Asking user if they want to run again ##
        while True:
            print(Fore.LIGHTGREEN_EX + "Would you like to request more data? " + Style.RESET_ALL + "(Yes/No):")
            again = input().strip().lower()
            if again in ["Yes", "Y", "yes", "YES"]:  ## User validation here is all different ways to say YES and NO ##
                print()
                break  ## Restarts the loop ##
            elif again in ["No", "n", "no", "NO"]:
                print("\nThank you!\n")
                return  ## Exits the program ##
            else:
                print("Please enter 'Yes' or 'No'.")



fake = Faker() ## Faker instance that generates types of fake data ##
data_fields = {
    "ID Number": lambda: random.randint(1, 99999), ## Each value here is a lambda function that returns a randomly generated piece of data for that field. ##
    "Username": lambda: fake.user_name(),
    "Full Name": lambda: fake.name(),
    "DOB (DD/MM/YYY)": lambda: fake.date_of_birth().strftime("%d/%m/%Y"), ## Date set for UK Region ##
    "Email": lambda: fake.email(),
    "Phone Number": lambda: fake.phone_number(),
    "Address": lambda: fake.address(),
    "IPv4 Address": lambda: fake.ipv4(),
}


def display_field_options():
    print()
    print(Fore.LIGHTGREEN_EX + "Please pick from the list of data fields you would like to generate:" + Style.RESET_ALL)
    print()
    for i, field in enumerate(data_fields.keys(), 1): ## Displays the field options to the user from the list of fields above ##
        print(f"{i}. {field}")
    print()


def get_user_field_selection():
    while True:
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


def generate_data(fields, count):
    result = []
    for _ in range(count):
        obj = {field: data_fields[field]() for field in fields} ## Generates a fake data record using the selected fields ##
        result.append(obj)
    return result


def export_to_ndjson(data, filename="data.ndjson"):
    with open(filename, "w") as f:
        for obj in data:
            json_line = json.dumps(obj) ## Puts the dictionary to a NDJSON formatted string ##
            f.write(json_line + "\n") ## Writes it to the file one record per line in NDJSON format ##
    print(Fore.LIGHTGREEN_EX + f"\nSuccess! " + Style.RESET_ALL + f"File exported to '{filename}'\n") ## Displays exported filename ##



if __name__ == "__main__": ## Runs the main() function only if this script is run directly ##
    main()
