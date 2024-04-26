import numpy as np

def calculate_priorities(transportation_matrix):
    row_means = np.mean(transportation_matrix, axis=1) # Calculate mean of each row
    
    col_means = np.mean(transportation_matrix, axis=0) # Calculate mean of each column
    
    means_array = np.concatenate((row_means, col_means)) # Concatenate row and column means

    priority_array = np.arange(1, len(means_array) + 1) # Create an array of numbers from 1 to len(means_array)
    
    # Sort the means_array along with their indices
    sorted_indices = np.argsort(means_array)
    sorted_means = means_array[sorted_indices]
    
    # Assign priorities to each value in means_array
    current_priority = 1
    for i in range(len(sorted_means)):
        if i > 0 and sorted_means[i] == sorted_means[i - 1]:
            # If the current value is equal to the previous one, assign the next sequential priority
            current_priority += 1
        else:
            # Otherwise, assign a new priority
            current_priority = max(current_priority, i + 1)  # Ensure sequential priorities
        priority_array[sorted_indices[i]] = current_priority
    
    return priority_array

# Example usage:
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
priorities = calculate_priorities(matrix)
print("Priorities array:", priorities)
