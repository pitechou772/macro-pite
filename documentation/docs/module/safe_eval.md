# Module : Évaluation sécurisée d'expressions

## `safe_eval_expr(expr, variables=None)`

Évalue une expression arithmétique, logique ou de comparaison en toute sécurité avec support des variables.

**Paramètres :**
- `expr` *(str)* : Expression à évaluer (arithmétique, logique, comparaison)
- `variables` *(dict)* : Dictionnaire des variables disponibles

**Retour :**
- Résultat de l'évaluation (nombre, booléen, etc.)

**Fonctionnalités supportées :**
- **Opérateurs arithmétiques** : `+`, `-`, `*`, `/`, `%`, `-` (négation)
- **Opérateurs de comparaison** : `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Opérateurs logiques** : `and`, `or`, `not`
- **Variables** : Support des variables avec préfixe `$`

**Exemples :**
```python
safe_eval_expr("10 + 5 * 2", {})  # → 20
safe_eval_expr("$x > 5", {"$x": 10})  # → True
safe_eval_expr("$a and $b", {"$a": True, "$b": False})  # → False
```

---

## `_eval_ast(node, env=None)`

Fonction interne qui évalue récursivement un AST Python de manière sécurisée.

**Paramètres :**
- `node` *(ast.AST)* : Nœud AST à évaluer
- `env` *(dict)* : Environnement de variables

**Sécurité :**
- Seuls les opérateurs autorisés sont supportés
- Pas d'accès aux fonctions système
- Évaluation contrôlée des expressions

---

## Opérateurs autorisés

### Arithmétiques (OPS)
- `ast.Add` : Addition (`+`)
- `ast.Sub` : Soustraction (`-`)
- `ast.Mult` : Multiplication (`*`)
- `ast.Div` : Division (`/`)
- `ast.Mod` : Modulo (`%`)
- `ast.USub` : Négation (`-`)

### Comparaisons (CMP_OPS)
- `ast.Eq` : Égalité (`==`)
- `ast.NotEq` : Inégalité (`!=`)
- `ast.Lt` : Inférieur (`<`)
- `ast.LtE` : Inférieur ou égal (`<=`)
- `ast.Gt` : Supérieur (`>`)
- `ast.GtE` : Supérieur ou égal (`>=`)

### Logiques (BOOL_OPS)
- `ast.And` : ET logique (`and`)
- `ast.Or` : OU logique (`or`)
