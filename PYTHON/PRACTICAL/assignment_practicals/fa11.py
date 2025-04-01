import numpy as np

def temperature_analysis():
    # Input
    N, M = map(int, input().split())
    temperature_data = []
    
    for _ in range(N):
        city_temps = list(map(int, input().split()))
        temperature_data.append(city_temps)
    
    # Convert to numpy array
    temp_matrix = np.array(temperature_data)
    
    # 1. Flatten the temperature matrix
    flattened = temp_matrix.flatten()
    print(flattened)
    
    # 2. Find hottest and coldest temperatures
    hottest = np.max(temp_matrix)
    coldest = np.min(temp_matrix)
    print(f"Hottest Temperature: {hottest}")
    print(f"Coldest Temperature: {coldest}")
    
    # 3. Average temperature for each city (row-wise)
    city_averages = np.mean(temp_matrix, axis=1)
    print(city_averages)
    
    # 4. Average temperature for each day (column-wise)
    day_averages = np.mean(temp_matrix, axis=0)
    print(day_averages)
    
    # 5. Normalize the data using min-max scaling
    min_temp = np.min(temp_matrix)
    max_temp = np.max(temp_matrix)
    normalized = (temp_matrix - min_temp) / (max_temp - min_temp)
    print(normalized)
    
    # 6. Transpose the data
    transposed = np.transpose(temp_matrix)
    print(transposed)
    
    # 7. Add new temperature readings for an extra day
    new_day = np.array([[34], [32], [29]])  # Example extra day data
    expanded = np.append(temp_matrix, new_day, axis=1)
    print(expanded)
    
    # 8. Remove the coldest day's data
    coldest_day_index = np.argmin(np.mean(temp_matrix, axis=0))
    reduced = np.delete(temp_matrix, coldest_day_index, axis=1)
    print(reduced)

temperature_analysis()