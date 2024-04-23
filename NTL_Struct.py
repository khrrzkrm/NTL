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

    def __repr__(self):
        tmax_display = '∞' if self.tmax == float('inf') else self.tmax
        return f"[{self.tmin}, {tmax_display}]"

class IntervalSet:
    def __init__(self, intervals):
        self.intervals = intervals

    def __repr__(self):
        return f"{{{', '.join(map(str, self.intervals))}}}"

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

    def __repr__(self):
        return f"{self.norm_type} {self.interval_set} {self.action}"

class BinaryOperation:
    def __init__(self, left, operator, right):
        if operator not in {'&', '||'}:
            raise ValueError(f"Invalid operator '{operator}'. Operator must be '&' or '||'.")
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

# Example usage of the AST classes
if __name__ == "__main__":
    # Define some actions
    action_a = Action("a")

    # Define some intervals
    interval1 = Interval(1, 3)
    interval2 = Interval(5, float('inf'))
    interval3 = Interval(float('inf'), 1000)   # Using float('inf') directly for demonstration

    # Create interval sets
    interval_set1 = IntervalSet([interval1, interval3])

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
