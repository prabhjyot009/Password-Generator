import string
import random
import math

def generate_password(length):
    charset = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(charset) for i in range(length))
    return password

def password_strength(password):
    length = len(password)
    length_score = 10 * (1 - math.exp(-length / 10))

    uppercase = False
    lowercase = False
    digit = False
    special_char = False
    for c in password:
        if c.isupper():
            uppercase = True
        elif c.islower():
            lowercase = True
        elif c.isdigit():
            digit = True
        elif not c.isalnum():
            special_char = True
    complexity_score = 0
    if uppercase:
        complexity_score += 2
    if lowercase:
        complexity_score += 2
    if digit:
        complexity_score += 2
    if special_char:
        complexity_score += 4

    entropy = 0
    if length > 0:
        character_set_size = len(set(password))
        entropy = length * math.log2(character_set_size)
    randomness_score = (entropy / 128) * 100

    with open('dictionary.txt', 'r') as file:
        dictionary = set(line.strip() for line in file)
    words = set(password.split())
    dictionary_score = 0
    for word in words:
        if word in dictionary:
            dictionary_score = -20
            break

    common_substitutions = {
        'a': '@',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '$'
    }
    substitution_score = 0
    for key, value in common_substitutions.items():
        if key in password or value in password or value.upper() in password:
            substitution_score -= 10
            break

    personal_info = {
        'password', '123456', 'qwerty', 'abc123', 'letmein',
        'monkey', 'football', 'iloveyou', 'admin'
    }
    personal_score = 0
    lowercase_password = password.lower()
    if lowercase_password in personal_info:
        personal_score -= 20

    reused_passwords = {
        'password1', 'password2', 'password3', 'password4', 'password5'
    }
    reused_score = 0
    if lowercase_password in reused_passwords:
        reused_score -= 10

    pattern_score = 0
    if (set('0123456789').isdisjoint(password) or
        set('abcdefghijklmnopqrstuvwxyz').isdisjoint(password) or
        set('ABCDEFGHIJKLMNOPQRSTUVWXYZ').isdisjoint(password) or
        set(password).issubset(string.ascii_letters + string.digits)):
        pattern_score -= 10

    score = length_score + complexity_score + randomness_score + \
            dictionary_score + substitution_score + personal_score + \
            reused_score + pattern_score

    # Cap the score at 100 if it exceeds that value
    return min(round(score), 100)

if __name__ == '__main__':
    password = input("Enter the password (or press '1' to generate a random password):\n")
    if password == '1':
        password_length = int(input("Enter the length of the generated password:\n"))
        if password_length <= 0:
            print("Invalid password length. Please enter a positive integer.")
        else:
            password = generate_password(password_length)
            print("Generated Password:", password)
    else:
        strength = password_strength(password)
        print("Password strength:", strength)