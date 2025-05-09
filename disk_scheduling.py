def fcfs(requests, head):

    total_seek_time = 0
    current_head = head
    movement_sequence = [head]
    
    for request in requests:
        # Calculate seek time 
        seek_time = abs(current_head - request)
        total_seek_time += seek_time
        
        # Move head to the requested position
        current_head = request
        movement_sequence.append(current_head)
    
    return total_seek_time, movement_sequence


def scan(requests, head, num_cylinders, direction):
    total_seek_time = 0
    current_head = head
    movement_sequence = [head]
    
    # Sort requests for processing
    remaining_requests = sorted(requests)
    
    # Determine the requests greater and smaller than the head position
    smaller_requests = [r for r in remaining_requests if r < head]
    greater_requests = [r for r in remaining_requests if r > head]
    
    # Determine the sequence based on direction
    if direction == 'outer':  
        service_sequence = greater_requests
       
        if smaller_requests:
            service_sequence += [num_cylinders - 1]  # Go to the end
            service_sequence += sorted(smaller_requests, reverse=True)  # Then go back serving requests
    else:  # Moving toward lower cylinder numbers first
       
        service_sequence = sorted(smaller_requests, reverse=True)
       
        if greater_requests:
            service_sequence += [0]  # Go to the beginning
            service_sequence += greater_requests  # Then go back serving requests
    
    # Calculate seek time and build movement sequence
    for request in service_sequence:
        seek_time = abs(current_head - request)
        total_seek_time += seek_time
        current_head = request
        movement_sequence.append(current_head)
    
    return total_seek_time, movement_sequence


def c_scan(requests, head, num_cylinders, direction):
   
    total_seek_time = 0
    current_head = head
    movement_sequence = [head]
    
    # Sort requests for processing
    remaining_requests = sorted(requests)
    
    # Determine the requests greater and smaller than the head position
    smaller_requests = [r for r in remaining_requests if r < head]
    greater_requests = [r for r in remaining_requests if r > head]
    
    # Determine the sequence based on direction
    if direction == 'outer': 
        service_sequence = greater_requests
        
        # Go to the end and quickly move to the beginning (circular seek)
        if smaller_requests:
            service_sequence += [num_cylinders - 1] 
            service_sequence += [0]  
            service_sequence += smaller_requests  # Then process remaining requests
    else:  
        service_sequence = sorted(smaller_requests, reverse=True)
        
        # Go to beginning and quickly move to the end (circular seek)
        if greater_requests:
            service_sequence += [0]  
            service_sequence += [num_cylinders - 1]  
            service_sequence += sorted(greater_requests, reverse=True)
    
    # Calculate seek time and build movement sequence
    prev_request = current_head
    for request in service_sequence:
        # Skip calculating seek time for the circular jump
        if (prev_request == num_cylinders - 1 and request == 0) or \
           (prev_request == 0 and request == num_cylinders - 1):
            movement_sequence.append(request)
            prev_request = request
            continue
            
        seek_time = abs(prev_request - request)
        total_seek_time += seek_time
        prev_request = request
        movement_sequence.append(request)
    
    return total_seek_time, movement_sequence


def main():
    print("Disk Scheduling Algorithms Simulator")
    print("------------------------------------")
    
    # Get user inputs
    queue_size = int(input("Enter the number of disk requests: "))
    head_position = int(input("Enter the initial position of disk head: "))
    num_cylinders = int(input("Enter the number of cylinders (0 to n-1): "))
    
    print("Enter the disk requests (cylinder numbers):")
    requests = []
    for i in range(queue_size):
        request = int(input(f"Request {i+1}: "))
        if request < 0 or request >= num_cylinders:
            print(f"Invalid request. Cylinder number must be between 0 and {num_cylinders-1}")
            return
        requests.append(request)
    
    print("\nSelect the disk scheduling algorithm:")
    print("1. FCFS (First-Come-First-Served)")
    print("2. SCAN (Elevator)")
    print("3. C-SCAN (Circular SCAN)")
    algorithm = int(input("Enter your choice (1-3): "))
    
    direction = None
    if algorithm in [2, 3]:
        print("\nSelect initial direction of head movement:")
        print("1. Toward outer tracks (increasing cylinder numbers)")
        print("2. Toward inner tracks (decreasing cylinder numbers)")
        dir_choice = int(input("Enter your choice (1-2): "))
        direction = 'outer' if dir_choice == 1 else 'inner'
    
    # Execute the selected algorithm
    if algorithm == 1:
        total_seek_time, movement_sequence = fcfs(requests, head_position)
        algorithm_name = "FCFS"
    elif algorithm == 2:
        total_seek_time, movement_sequence = scan(requests, head_position, num_cylinders, direction)
        algorithm_name = f"SCAN (direction: {direction})"
    elif algorithm == 3:
        total_seek_time, movement_sequence = c_scan(requests, head_position, num_cylinders, direction)
        algorithm_name = f"C-SCAN (direction: {direction})"
    else:
        print("Invalid algorithm choice!")
        return
    
    # Display results
    print("\nResults:")
    print(f"Algorithm: {algorithm_name}")
    print(f"Total Seek Time: {total_seek_time}")
    print("Order of requests served:")
    print(" -> ".join(map(str, movement_sequence)))


if __name__ == "__main__":
    main()
