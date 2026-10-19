import argparse
from utils import TruthValue
from engine import prove

def visualize():
	print("option is enabled")

class Fact:
	def __init__(self, name):
		self.name = name
		self.initial = False
		self.rules = []
		
class Rule:
	def __init__(self, condition, conclusion):
		self.condition = condition
		self.conclusion = conclusion
		
class Expression:
	def __init__(self, operator, left=None, right=None):
		self.operator = operator
		self.left = left
		self.right = right
  
def get_facts_from_expression(expr):
	if expr.operator == "FACT":
		return [expr.left]
	facts = []
	if expr.left is not None:
		facts.extend(get_facts_from_expression(expr.left))
	if expr.right is not None:
		facts.extend(get_facts_from_expression(expr.right))
	return facts

def get_fact(facts, name):
	if name not in facts:
		facts[name] = Fact(name)
	return facts[name]
		
def parse_rule(rule, facts):
	rule = rule.strip()
	if "<=>" in rule:
		left, right = rule.split("<=>", 1)
		rule1 = parse_rule(left + " => " + right, facts)
		rule2 = parse_rule(right + " => " + left, facts)
		return [rule1, rule2]
	condition, conclusion = rule.split("=>", 1)
	condition_expr = parse_expression(condition, facts)
	conclusion_expr = parse_expression(conclusion, facts)
	rule = Rule(condition_expr, conclusion_expr)
	for fact in get_facts_from_expression(conclusion_expr):
		fact.rules.append(rule)
	print("RULE:", rule)
	print("CONDITION:", condition_expr.operator)
	print("CONCLUSION:", conclusion_expr.operator)
	print("CONCLUSION FACTS:", [f.name for f in get_facts_from_expression(conclusion_expr)])
	return [rule]

def parse_file(filename):
	facts = {}
	rules = []
	queries = []
	with open(filename, "r") as file:
		for line in file:
			line = line.strip()
			if not line:
				continue
			if line.startswith("="):
				for char in line[1:]:
					if char not in facts:
						facts[char] = Fact(char)
					facts[char].initial = True
			elif line.startswith("?"):
				for char in line[1:]:
					queries.append(char)
			elif "=>" in line:
				rules.append(line)
			else:
				raise ValueError(f"Invalid line: {line}")
	return facts, rules, queries

def strip_outer_parentheses(expression):
    """Retire les parenthèses extérieures si elles englobent toute l'expression."""
    expression = expression.strip()
    while expression.startswith("(") and expression.endswith(")"):
        depth = 0
        wraps_all = True
        for i, char in enumerate(expression):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if depth < 0:
                raise ValueError("Parenthèses mal fermées")
            if depth == 0 and i != len(expression) - 1:
                wraps_all = False
                break
        if depth != 0:
            raise ValueError("Parenthèses mal fermées")
        if not wraps_all:
            break
        expression = expression[1:-1].strip()
    return expression

def find_top_level_operator(expression, operator):
    """Trouve un opérateur situé hors des parenthèses."""
    depth = 0
    for i, char in enumerate(expression):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("Parenthèses mal fermées")
        elif char == operator and depth == 0:
            return i
    if depth != 0:
        raise ValueError("Parenthèses mal fermées")
    return -1

def parse_expression(expression, facts):
    expression = expression.strip()
    if not expression:
        raise ValueError("Expression vide")
    expression = strip_outer_parentheses(expression)
    if expression.startswith("!"):
        operand = parse_expression(expression[1:], facts)
        return Expression("NOT", operand)
    for operator, name in [("^", "XOR"), ("|", "OR"), ("+", "AND"), ]:
        pos = find_top_level_operator(expression, operator)
        if pos != -1:
            left = parse_expression(expression[:pos], facts)
            right = parse_expression(expression[pos + 1:], facts)
            return Expression(name, left, right)
    if any(char in expression for char in "()!+|^"):
        raise ValueError(f"Expression invalide : {expression}")
    fact = get_fact(facts, expression)
    return Expression("FACT", fact)

def main():
	parser = argparse.ArgumentParser(description="backward chaining engine ")
	parser.add_argument("-v", "--visualize", action="store_true", help="Shows the reasoning")
	parser.add_argument("file", help="input file containing rules and queries")
	args = parser.parse_args()
	if args.visualize:
		visualize()
	facts, rules, queries = parse_file(args.file)
	parsed_rules = []
	for rule in rules:
		parsed_rules.extend(parse_rule(rule, facts))
	rules = parsed_rules
	for query in queries:
		fact = get_fact(facts, query)
		result = prove(fact)
		print(query)
		if result == TruthValue.TRUE:
			print(True)
		elif result == TruthValue.FALSE:
			print(False)
		else:
			print("Undetermined")
   
main()