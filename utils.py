import math
import random

# Generates a list of random numbers
# Where the numbers are in the range [min_value, max_value]
# and the total number of numbers (length of list) is total_numbers
def generate_exponential_numbers(min_value, max_value, total_numbers):
    numbers = []
    for i in range(total_numbers):
        y = random.randrange(min_value, max_value)
        number = int( (math.exp(-y ** 2 / max_value ** 2) * max_value)  )
        numbers.append(number)
        
    # Find the maximum and minimum values in the list
    min_number = min(numbers)
    max_number = max(numbers)
    # Map the values from the current range to the desired range (0 to 800)
    mapped_numbers = [int((number - min_number) * max_value / (max_number - min_number)) for number in numbers]
    # Sort and reverse to map to screen coordinates
    mapped_numbers.sort()
    mapped_numbers.reverse()

    return mapped_numbers
    
# Numpy version
import numpy as np

def generate_exponential_numbers(min_value, max_value, total_numbers, desired_range=800):
    # Generate random numbers with an exponential distribution
    y_values = np.random.randint(min_value, max_value, total_numbers)
    numbers = np.array(np.exp(-y_values ** 2 / max_value ** 2) * max_value, dtype=int)
    
    # Map values to the desired range
    min_number = np.min(numbers)
    max_number = np.max(numbers)
    mapped_numbers = ((numbers - min_number) * desired_range / (max_number - min_number)).astype(int)
    
    # Sort and reverse the mapped numbers
    mapped_numbers = np.sort(mapped_numbers)[::-1]

    return mapped_numbers.tolist()
