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
    mapped_numbers = [int((number - min_number) * 800 / (max_number - min_number)) for number in numbers]
    # Sort and reverse to map to screen coordinates
    mapped_numbers.sort()
    mapped_numbers.reverse()

    return mapped_numbers
