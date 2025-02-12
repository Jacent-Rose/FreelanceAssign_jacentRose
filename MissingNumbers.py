def findMissingNumber(arr):
    n = len(arr) + 1  # The array should have n elements, and one is missing
    xor_all = 0
    xor_arr = 0
    
    # XOR all numbers from 1 to n
    for i in range(1, n + 1):
        xor_all ^= i
    
    # XOR all numbers in the array
    for num in arr:
        xor_arr ^= num
    
    # The missing number will be the XOR of xor_all and xor_arr
    return xor_all ^ xor_arr

# Example
arr = [3, 7, 1, 2, 8, 4, 5]
print(findMissingNumber(arr))  # Output: 6
