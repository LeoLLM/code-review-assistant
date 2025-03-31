#!/usr/bin/env python3
# Example code with various issues for review practice

import time
import random
import os

# Global variables
password = "admin123"  # Security issue: Hardcoded credentials
DEBUG = True

def connect_to_database(user, pwd):
    """Connect to the database with the given credentials."""
    # Security issue: SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'"
    print(f"Executing query: {query}")
    # Simulate database connection
    time.sleep(1)
    return True

def process_data(data):
    """Process the input data."""
    # Performance issue: Inefficient algorithm (O(n²))
    result = []
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j and data[i] < data[j]:
                result.append((data[i], data[j]))
    return result

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    # Readability issue: Complex function without comments
    s = 0
    c = 0
    for n in numbers:
        if n != None and n != 0:  # Quality issue: Redundant condition, should use "if n is not None"
            s = s + n  # Style issue: Should use += operator
            c = c + 1
    if c == 0:
        return 0
    return s/c

# DRY issue: Repeated code
def validate_user_input(input_data):
    if input_data == "":
        print("Error: Empty input")
        return False
    return True

def validate_email_input(input_data):
    if input_data == "":
        print("Error: Empty input")
        return False
    if "@" not in input_data:
        print("Error: Invalid email")
        return False
    return True

# Error handling issue: No try-except
def read_config_file(filename):
    f = open(filename, 'r')  # Resource management issue: Not using 'with' statement
    content = f.read()
    f.close()
    return content

# Main function
def main():
    # Uncommented debugging code left in
    # print("Debug mode active")
    
    connect_to_database("user", password)
    
    # Hardcoded values that should be constants
    data = [random.randint(1, 100) for _ in range(1000)]
    
    start_time = time.time()
    results = process_data(data)
    end_time = time.time()
    
    if DEBUG:
        print(f"Processing took {end_time - start_time} seconds")  # Performance issue: No benchmarking
        print(f"Found {len(results)} pairs")
    
    return results

if __name__ == "__main__":
    main()