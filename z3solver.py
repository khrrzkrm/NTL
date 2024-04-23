from z3 import *

def parse_interval(interval_str):
    if interval_str.startswith('[') and interval_str.endswith(']'):
        contents = interval_str[1:-1].split(',')
        if len(contents) == 2:
            start, end = map(int, contents)
            return (start, end)
    return None

def intersect_intervals(intervals):
    if not intervals:
        return None
    intersected = intervals[0]
    for start, end in intervals[1:]:
        intersected_start, intersected_end = intersected
        if start > intersected_end or end < intersected_start:
            return None  # No intersection
        intersected = (max(start, intersected_start), min(end, intersected_end))
    return intersected

def difference_intervals(interval, intersection):
    """ Calculate the difference of two intervals, may return up to two disjoint intervals. """
    if not intersection:
        return [interval]
    start, end = interval
    inter_start, inter_end = intersection
    results = []
    if start < inter_start:
        results.append((start, min(end, inter_start - 1)))
    if end > inter_end:
        results.append((max(start, inter_end + 1), end))
    return results

s = Solver()
action_intervals = {}

print("Enter action and interval pairs (e.g., a,[1,10]). Input 'z,[]' to end.")

while True:
    user_input = input("Enter action and interval (action,[start,end]): ")
    if user_input == "z,[]":
        break

    action_part, interval_part = user_input.split(',', 1)
    interval = parse_interval(interval_part.strip())

    if action_part and interval:
        action = action_part.strip()
        if action not in action_intervals:
            action_intervals[action] = []
        action_intervals[action].append(interval)

# Process each action's intervals
for action, intervals in action_intervals.items():
    if len(intervals) < 2:
        continue  # Need at least two intervals to make sense of the specification
    intersection = intersect_intervals(intervals)
    time_var1 = Int(f't_{action}_1')
    time_var2 = Int(f't_{action}_2')

    if intersection:
        inter_start, inter_end = intersection
        # Model 1: Action occurs once within the intersection
        s.push()  # Create a new context
        s.add(time_var1 >= inter_start, time_var1 <= inter_end)
        if s.check() == sat:
            print(f"Satisfiable within intersection for {action}: {s.model()}")
        else:
            print(f"Unsatisfiable within intersection for {action}")
        s.pop()  # Remove the context

        # Model 2: Action occurs in each interval, reduced by intersection
        differences = []
        for interval in intervals:
            differences.extend(difference_intervals(interval, intersection))
        
        if differences:
            constraints = [Or(time_var1 >= start and time_var1 <= end for start, end in differences)]
            s.add(constraints)
            if s.check() == sat:
                print(f"Satisfiable in individual intervals for {action}: {s.model()}")
            else:
                print(f"Unsatisfiable in individual intervals for {action}")

