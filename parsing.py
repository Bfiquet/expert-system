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
  
def get_fact(facts, name):
	if name not in facts:
		facts[name] = Fact(name)
	return facts[name]

def parse_expression(expression, facts):
	expression = expression.strip()
	if "+" in expression:
		left, right = expression.split("+", 1)
		left = parse_expression(left, facts)
		right = parse_expression(right, facts)
		return Expression("AND", left, right)
	fact = get_fact(facts, expression)
	return Expression("FACT", fact)

def parse_rule(rule, facts):
	rule = rule.strip()
	condition, conclusion = rule.split("=>")
	condition = condition.strip()
	conclusion = conclusion.strip()
	condition_expr = parse_expression(condition, facts)
	conclusion_fact = get_fact(facts, conclusion)
	rule = Rule(condition_expr, conclusion_fact)
	conclusion_fact.rules.append(rule)
	return rule

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
		parsed_rules.append(parse_rule(rule, facts))
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