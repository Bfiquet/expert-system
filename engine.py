from utils import TruthValue

def prove(fact, visiting=None):
    if visiting is None:
        visiting = set()
    if fact.initial:
        return TruthValue.TRUE
    if fact in visiting:
        return TruthValue.UNDETERMINED
    visiting.add(fact)
    for rule in fact.rules:
        result = evaluate(rule.condition, visiting)
        if result != TruthValue.TRUE:
            continue
        if rule.conclusion.operator == "FACT":
            if rule.conclusion.left == fact:
                visiting.remove(fact)
                return TruthValue.TRUE
        elif rule.conclusion.operator == "AND":
            if contains_fact(rule.conclusion, fact):
                visiting.remove(fact)
                return TruthValue.TRUE
        elif rule.conclusion.operator in ("OR", "XOR"):
            continue
    visiting.remove(fact)
    if len(fact.rules) == 0:
        return TruthValue.UNDETERMINED
    for rule in fact.rules:
        if rule.conclusion.operator in ("OR", "XOR"):
            if evaluate(rule.condition, visiting) == TruthValue.TRUE:
                return TruthValue.UNDETERMINED
    return TruthValue.FALSE

def contains_fact(expr, fact):
	if expr.operator == "FACT":
		return expr.left == fact
	if expr.left is not None and contains_fact(expr.left, fact):
		return True
	if expr.right is not None and contains_fact(expr.right, fact):
		return True
	return False

def evaluate(expr, visiting):
    if expr.operator == "FACT":
        return prove(expr.left, visiting)

    if expr.operator == "NOT":
        result = evaluate(expr.left, visiting)

        if result == TruthValue.TRUE:
            return TruthValue.FALSE

        if result == TruthValue.FALSE:
            return TruthValue.TRUE

        return TruthValue.UNDETERMINED

    if expr.operator == "AND":
        left = evaluate(expr.left, visiting)
        right = evaluate(expr.right, visiting)

        if left == TruthValue.TRUE and right == TruthValue.TRUE:
            return TruthValue.TRUE

        return TruthValue.FALSE

    if expr.operator == "OR":
        left = evaluate(expr.left, visiting)
        right = evaluate(expr.right, visiting)

        if left == TruthValue.TRUE or right == TruthValue.TRUE:
            return TruthValue.TRUE

        return TruthValue.FALSE

    if expr.operator == "XOR":
        left = evaluate(expr.left, visiting)
        right = evaluate(expr.right, visiting)

        if (left == TruthValue.TRUE) != (right == TruthValue.TRUE):
            return TruthValue.TRUE

        return TruthValue.FALSE
    
	# def evaluate(expr):
# 	if expr.operator == "FACT":
# 		return prove(expr.left)
# 	if expr.operator == "NOT":
# 		result = evaluate(expr.left)
# 		if result == TruthValue.TRUE:
# 			return TruthValue.FALSE
# 		if result == TruthValue.FALSE:
# 			return TruthValue.TRUE
# 		return TruthValue.UNDETERMINED
# 	if expr.operator == "AND":
# 		left = evaluate(expr.left)
# 		right = evaluate(expr.right)
# 		if left == TruthValue.TRUE and right == TruthValue.TRUE:
# 			return TruthValue.TRUE
# 		return TruthValue.FALSE
# 	if expr.operator == "OR":
# 		left = evaluate(expr.left)
# 		right = evaluate(expr.right)
# 		if left == TruthValue.TRUE or right == TruthValue.TRUE:
# 			return TruthValue.TRUE
# 		return TruthValue.FALSE
# 	if expr.operator == "XOR":
# 		left = evaluate(expr.left)
# 		right = evaluate(expr.right)
# 		if (left == TruthValue.TRUE or right == TruthValue.TRUE) and left != right:
# 			return TruthValue.TRUE
# 		return TruthValue.FALSE
	