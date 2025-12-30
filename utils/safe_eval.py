"""
Safe Expression Evaluation Module
Supports arithmetic, comparisons, and boolean operations without using eval()
"""
import ast
import operator

# Supported operators
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg
}

CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge
}

BOOL_OPS = {
    ast.And: all,
    ast.Or: any
}


def safe_eval_expr(expr, variables=None):
    """
    Évalue une expression (arithmétique / logique) en toute sécurité.
    Supporte +, -, *, /, %, comparaisons, et, ou, not, et variables ($x).
    """
    variables = variables or {}
    expr = expr.strip()
    # Remplace les variables simples par des identifiants temporaires (pour parsing)
    # On remplace $var par var__val0 puis on injecte dans un env lors de l'évaluation
    env = {}
    idx = 0
    for k, v in variables.items():
        placeholder = f"_v{idx}"
        expr = expr.replace(k, placeholder)
        env[placeholder] = v
        idx += 1

    try:
        tree = ast.parse(expr, mode='eval')
        return _eval_ast(tree.body, env)
    except Exception as e:
        raise ValueError(f"Expression invalide : {expr} -> {e}")


def _eval_ast(node, env=None):
    """Evaluate AST node recursively"""
    env = env or {}
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):  # compat
        return node.n
    if isinstance(node, ast.Name):
        # récupère depuis env si présent
        return env.get(node.id, 0)
    if isinstance(node, ast.BinOp):
        if type(node.op) in OPS:
            return OPS[type(node.op)](_eval_ast(node.left, env), _eval_ast(node.right, env))
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return not _eval_ast(node.operand, env)
        if type(node.op) in OPS:
            return OPS[type(node.op)](_eval_ast(node.operand, env))
    if isinstance(node, ast.Compare):
        left = _eval_ast(node.left, env)
        result = True
        for op, comparator in zip(node.ops, node.comparators):
            if type(op) in CMP_OPS:
                right = _eval_ast(comparator, env)
                result = CMP_OPS[type(op)](left, right)
                left = right
            else:
                raise ValueError("Comparaison non supportée")
        return result
    if isinstance(node, ast.BoolOp):
        vals = [_eval_ast(v, env) for v in node.values]
        if type(node.op) in BOOL_OPS:
            func = BOOL_OPS[type(node.op)]
            # and -> all, or -> any ; on considère les valeurs truthy
            return func([bool(v) for v in vals])
    raise ValueError("Opération non supportée dans expression")


def check_variable_exists(var_name, variables):
    """Check if a variable exists in the variables dict"""
    return var_name in variables
