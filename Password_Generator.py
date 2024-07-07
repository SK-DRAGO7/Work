import random
import string

def generate_password(length, include_uppercase=True, include_digits=True, include_special_chars=True):
    # Define the character sets to use
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if include_uppercase else ""
    digits = string.digits if include_digits else ""
    special_chars = string.punctuation if include_special_chars else ""

    # Combine all the characters
    all_chars = lower + upper + digits + special_chars

    # Ensure there is at least one character type included
    if not all_chars:
        raise ValueError("At least one character type must be included.")

    # Generate the password
    password = "".join(random.choice(all_chars) for _ in range(length))

    return password

# Example usage
if __name__ == "__main__":
    try:
        length = int(input("Enter the desired password length: "))
        include_uppercase = input("Include uppercase letters? (yes/no): ").strip().lower() == 'yes'
        include_digits = input("Include digits? (yes/no): ").strip().lower() == 'yes'
        include_special_chars = input("Include special characters? (yes/no): ").strip().lower() == 'yes'

        password = generate_password(length, include_uppercase, include_digits, include_special_chars)
        print("Generated Password:", password)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("An error occurred:", e)
