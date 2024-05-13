from z3 import Or as Zor
class Interval:
    def __init__(self, tmin, tmax):
        # Validate tmax as either an integer or 'inf'
        if not (isinstance(tmax, int) or tmax == float('inf')):
            raise ValueError(f"Invalid tmax '{tmax}'. tmax must be an integer or 'inf'.")
        if tmax == 'inf':
            tmax = float('inf')
        # Validate tmin is less than or equal to tmax
        if not isinstance(tmin, int) or tmin > tmax:
            raise ValueError(f"Invalid interval with tmin {tmin} and tmax {tmax}. tmin must be an integer and tmin <= tmax.")
        self.tmin = tmin
        self.tmax = tmax
    def add(self, i):
        new_tmin = self.tmin + i
        # Handle infinity case
        if self.tmax == float('inf'):
            new_tmax = float('inf')
        else:
            new_tmax = self.tmax + i
        return Interval(new_tmin, new_tmax)
    def __repr__(self):
        tmax_display = '∞' if self.tmax == float('inf') else self.tmax
        return f"[{self.tmin}, {tmax_display}]"

class IntervalSet:
    def __init__(self, intervals):
        self.intervals = intervals
    def max_value(self):
        # Extracts the tmax from each interval and finds the maximum
        max_val = max(interval.tmax for interval in self.intervals)
        return max_val if max_val != float('inf') else '∞'
    def __repr__(self):
        return f"{{{', '.join(map(str, self.intervals))}}}"
    def add(self, i):
        # Add a value to all intervals in the set and return a new IntervalSet
        new_intervals = [interval.add(i) for interval in self.intervals]
        return IntervalSet(new_intervals)    

class Action:
    def __init__(self, action):
        self.action = action
    def __repr__(self):
        return self.action

class Norm:
    def __init__(self, norm_type, interval_set, action):
        if norm_type not in {'O', 'F'}:
            raise ValueError(f"Invalid norm_type '{norm_type}'. Must be 'O' for Obligation or 'F' for Prohibition.")
        self.norm_type = norm_type
        self.interval_set = interval_set
        self.action = action
    def add(self, i):
        # Add a value to the intervals in the set and return a new Norm object
        new_interval_set = self.interval_set.add(i)
        return Norm(self.norm_type, new_interval_set, self.action)    
    def __repr__(self):
        return f"{self.norm_type} {self.interval_set} {self.action}"

class BinaryOperation:
    def __init__(self, left, operator, right):
        if operator not in {';', '||','&'}:
            raise ValueError(f"Invalid operator '{operator}'. Operator must be ';' or '&' or '||'.")
        self.left = left
        self.operator = operator
        self.right = right
    def add(self, i):
        new_left = self.left.add(i) if hasattr(self.left, 'add') else self.left + i
        new_right = self.right.add(i) if hasattr(self.right, 'add') else self.right + i
        return BinaryOperation(new_left, self.operator, new_right)
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"
    
    def count_obligations(self):
        # Recursively count the number of obligations in the binary operation
        if isinstance(self.left, Norm) and self.left.norm_type == 'O':
            count_left = 1
        elif hasattr(self.left, 'count_obligations'):
            count_left = self.left.count_obligations()
        else:
            count_left = 0

        if isinstance(self.right, Norm) and self.right.norm_type == 'O':
            count_right = 1
        elif hasattr(self.right, 'count_obligations'):
            count_right = self.right.count_obligations()
        else:
            count_right = 0

        return count_left + count_right
    
    def get_actions(self):
        # Recursively collect the set of actions present in the binary operation
        actions = set()
        if isinstance(self.left, Action):
            actions.add(self.left.action)
        elif hasattr(self.left, 'get_actions'):
            actions.update(self.left.get_actions())
        if isinstance(self.right, Action):
            actions.add(self.right.action)
        elif hasattr(self.right, 'get_actions'):
            actions.update(self.right.get_actions())

        return actions


    
def count_obligations(binary_op):
    if isinstance(binary_op, Norm):
        return 1 if binary_op.norm_type == 'O' else 0
    elif isinstance(binary_op, BinaryOperation):
        left_count = count_obligations(binary_op.left)
        right_count = count_obligations(binary_op.right)
        return left_count + right_count
    else:
        return 0
    
def get_alphabet(binary_op) -> list[str]:
    def recursive_get_alphabet(op) -> set:
        if isinstance(op, Norm):
            return {op.action}  
        elif isinstance(op, BinaryOperation):
            left_alphabet = recursive_get_alphabet(op.left)
            right_alphabet = recursive_get_alphabet(op.right)
            return left_alphabet.union(right_alphabet)  # Union of sets merges them without duplicates
        else:
            return set()
    # Convert the set of actions to a list before returning
    return list(recursive_get_alphabet(binary_op))
    
def print_actions(self):
    actions = self.get_actions()
    for action in actions:
        print(action)
# Example usage of the AST classes
if __name__ == "__main__":
    # Define some actions
    action_a = Action("a")

    # Define some intervals
    interval1 = Interval(1, 3)
    interval2 = Interval(5, float('inf'))

    # Create interval sets
    interval_set1 = IntervalSet([interval1, interval2])

    # Create norms
    obligation = Norm("O", interval_set1, action_a)
    prohibition = Norm("F", interval_set1, action_a)

    # Create binary operations
    conjunction = BinaryOperation(obligation, '&', prohibition)
    disjunction = BinaryOperation(obligation, '||', prohibition)

    # Print the constructed expressions
    print(obligation)  # Output: O {[1, 3], [5, ∞]} a
    print(prohibition)  # Output: F {[1, 3], [5, ∞]} a
    print(conjunction)  # Output: (O {[1, 3], [5, ∞]} a & F {[1, 3], [5, ∞]} a)
    print(disjunction)  # Output: (O {[1, 3], [5, ∞]} a || F {[1, 3], [5, ∞]} a)
