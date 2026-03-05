import random

def objective_function(x):
    """The function to maximize: f(x) = -x^2 + 5x + 10"""
    [span_3](start_span)return -x**2 + 5*x + 10[span_3](end_span)

def hill_climbing(step_size=0.1, max_iterations=1000):
    # 1. [span_4](start_span)Initialization: Start with a random initial state[span_4](end_span)
    current_x = random.uniform(-10, 10) 
    [span_5](start_span)current_value = objective_function(current_x)[span_5](end_span)
    
    print(f"Starting at x = {current_x:.4f}, f(x) = {current_value:.4f}")

    # 3. [span_6](start_span)Loop: Repeat until no better neighbors are found[span_6](end_span)
    for i in range(max_iterations):
        # Select neighbors (one step to the left, one to the right)
        next_x_left = current_x - step_size
        next_x_right = current_x + step_size
        
        # [span_7](start_span)Calculate values of neighbors[span_7](end_span)
        val_left = objective_function(next_x_left)
        val_right = objective_function(next_x_right)
        
        # 4. [span_8](start_span)[span_9](start_span)Compare and Move: Greedy approach[span_8](end_span)[span_9](end_span)
        if val_left > current_value and val_left >= val_right:
            current_x = next_x_left
            current_value = val_left
        elif val_right > current_value:
            current_x = next_x_right
            current_value = val_right
        else:
            # [span_10](start_span)Termination: Stop if no neighbor is better[span_10](end_span)
            print(f"Reached local maximum at iteration {i}")
            break
            
    return current_x, current_value

# Execute the algorithm
best_x, max_val = hill_climbing()

print("-" * 30)
print(f"Optimal x found: {best_x:.4f}")
print(f"Maximum value f(x): {max_val:.4f}")
