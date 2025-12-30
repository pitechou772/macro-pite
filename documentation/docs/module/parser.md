# Module : Parser de scripts

## `parse_script(script)`

Analyse un script macro et retourne la liste d'actions structurées avec les variables définies.

**Paramètres :**
- `script` *(str)* : Contenu texte du script

**Retour :**
- `tuple` : (actions, variables)
  - `actions` : Liste d'actions (chaînes ou tuples pour structures de contrôle)
  - `variables` : Dictionnaire des variables définies

**Fonctionnalités :**
- **Variables** : Définition avec `$nom = expression`
- **Structures de contrôle** : `if/elseif/else/endif`, `while/endwhile`, `loop/endloop`
- **Commentaires** : Lignes commençant par `#`
- **Indentation** : Support de l'indentation pour les blocs
- **Expressions** : Évaluation sécurisée des expressions dans les variables

**Exemple :**
```python
script = """
$count = 5
loop, $count
    echo, Itération $i
    wait, 1
endloop
"""
actions, variables = parse_script(script)
# actions = [('LOOP', 5, ['echo, Itération $i', 'wait, 1'])]
# variables = {'$count': 5}
```

---

## `replace_vars_runtime(line, vars_dict=None, loop_vars=None, system_vars=None)`

Remplace les variables dans une ligne au moment de l'exécution.

**Paramètres :**
- `line` *(str)* : Ligne de commande
- `vars_dict` *(dict)* : Variables définies lors du parsing
- `loop_vars` *(dict)* : Variables de boucle (ex: `$i`)
- `system_vars` *(dict)* : Variables système (ex: `$mouse_x`)

**Retour :**
- `str` : Ligne avec variables remplacées

**Variables système disponibles :**
- `$mouse_x`, `$mouse_y` : Position de la souris
- `$screen_width`, `$screen_height` : Résolution de l'écran

---

## Structures de contrôle supportées

### Boucles
```python
# loop, <count>, <block>
('LOOP', count, block_actions)
```

### Conditions
```python
# if/elseif/else/endif
('IF', [(condition, block), ('else', block), ...])
```

### Boucles while
```python
# while, <condition>, <block>
('WHILE', condition, block_actions)
```

### Contrôle de flux
```python
'BREAK'    # Sort de la boucle
'CONTINUE' # Passe à l'itération suivante
```

---

## Fonction interne : `parse_block(start, base_indent)`

Parse récursivement un bloc d'actions avec gestion de l'indentation.

**Paramètres :**
- `start` *(int)* : Index de début dans la liste des lignes
- `base_indent` *(int)* : Niveau d'indentation de base

**Retour :**
- `tuple` : (actions, next_index)
