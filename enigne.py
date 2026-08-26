from parsing import TruthValue

parser fichier.
prouver qqch: 
    partir de ce qu'on doit prouver
    remonter avec les regles
    explorer tous les chemins
    si possible de prouver true 
    sinon false 
    si pas de reglesm undetermined
    
gerer boucles infinies

def prove(fact):
    if fact.initial:
        return TruthValue.TRUE
    for rule in fact.rules:
        result = evaluate(rule.condition)
        if result == TruthValue.TRUE:
            return TruthValue.TRUE
    return TruthValue.FALSE

def evaluate(expr):
    if expr.operator == "FACT":
        return prove(expr.left)

    if expr.operator == "AND":
        left = evaluate(expr.left)
        right = evaluate(expr.right)

        if left == TruthValue.TRUE and right == TruthValue.TRUE:
            return TruthValue.TRUE

        return TruthValue.FALSE