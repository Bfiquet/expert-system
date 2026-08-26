import argparse
from enum import Enum

def visualize():
	print("option is enabled")

class TruthValue(Enum):
    TRUE = 1
    FALSE = 2
    UNDETERMINED = 3

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

def parse_rule(rule):
    rule = rule.strip()
    condition, conclusion = rule.split("=>")
    condition = condition.strip()
    conclusion = conclusion.strip()
    print("condition:", condition)
    print("conclusion:", conclusion)

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
                queries.append(line[1:])
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
	for rule in rules:
		parse_rule(rule)
	print("Facts : ", facts)
	print("Rules : ", rules)
	print("Queries : ", queries)

main()