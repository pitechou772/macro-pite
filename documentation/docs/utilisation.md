# Guide d'utilisation

## Écrire un script macro

Les scripts sont écrits ligne par ligne avec support des structures de contrôle avancées.

### Exemple de script complet :
```
# Définition de variables
$count = 5
$delay = 0.5

# Boucle simple
loop, $count
    echo, Itération $i
    type, Bonjour monde
    wait, $delay
    click, 100, 200, left
endloop

# Condition avec if/elseif/else
if, $count > 3
    echo, Nombre élevé
elseif, $count > 1
    echo, Nombre moyen
else
    echo, Nombre faible
endif

# Boucle while
while, $mouse_x < 500
    move, $mouse_x + 10, $mouse_y
    wait, 0.1
endwhile
```

## Commandes de base

### Clavier
- `press,<touche>,<durée>` : Maintient une touche pendant une durée
- `hotkey,<t1>+<t2>+...` : Appuie simultanément plusieurs touches
- `type,<texte>` : Tape du texte caractère par caractère

### Souris
- `click,<x>,<y>,<bouton>` : Clic à une position (left/right/middle)
- `lmc` / `rmc` / `mmc` : Clic gauche/droit/milieu à la position actuelle
- `move,<x>,<y>` : Déplace la souris à une position
- `scroll,<direction>,<quantité>` : Scroll (up/down)
- `on,<bouton>` / `off,<bouton>` : Maintenir/relâcher un bouton

### Contrôle
- `wait,<secondes>` : Pause
- `echo,<message>` : Affiche un message dans la console
- `input,<message>,<variable>` : Demande une saisie utilisateur (ancienne syntaxe)

### Saisie utilisateur (nouvelles fonctionnalités)
- `$var = input,<message>` : **Syntaxe recommandée** - Demande une saisie via boîte de dialogue

**Fonctionnement des boîtes de dialogue :**
- Une fenêtre pop-up s'ouvre avec le message
- L'utilisateur saisit la valeur et clique "OK"
- La valeur est automatiquement stockée dans la variable
- Si l'utilisateur annule, la variable reçoit une chaîne vide
- **Thread-safe** : Fonctionne correctement même pendant l'exécution de macros

**Exemples de saisie :**
```
$nom = input, "Entrez votre nom"
$age = input, "Entrez votre âge"
$email = input, "Entrez votre email"

# Utilisation des variables saisies
echo, Bonjour $nom
echo, Vous avez $age ans
type, $email
```

## Variables

### Définition
```
$nom = valeur
$count = 5
$message = "Bonjour"
$position = 100 + 50
```

### Variables système (automatiques)
- `$mouse_x`, `$mouse_y` : Position actuelle de la souris
- `$screen_width`, `$screen_height` : Résolution de l'écran
- `$i` : Index de boucle (dans les boucles loop)

### Variables de boucle
Dans une boucle `loop`, la variable `$i` contient l'index actuel (0, 1, 2, ...)

### Variables avec input (interface utilisateur)
```
# Syntaxe moderne (recommandée)
$age = input, "Entrez votre âge"
$nom = input, "Entrez votre nom"
echo, Bonjour $nom, vous avez $age ans

# Syntaxe alternative (supportée)
input, "Entrez votre ville", $ville
echo, Vous habitez à $ville
```

**Avantages de la nouvelle syntaxe :**
- Plus intuitive et cohérente
- Gestion automatique des erreurs
- Interface utilisateur moderne
- Thread-safe et stable

## Structures de contrôle

### Boucles
```
# Boucle simple
loop, 5
    type, Itération $i
    wait, 1
endloop

# Boucle infinie
loop, infinite
    echo, Boucle infinie
    wait, 1
endloop
```

### Conditions
```
# Structure if/elseif/else
if, $count > 10
    echo, Nombre élevé
elseif, $count > 5
    echo, Nombre moyen
else
    echo, Nombre faible
endif
```

### Boucles while
```
# Boucle conditionnelle
while, $mouse_x < 800
    move, $mouse_x + 10, $mouse_y
    wait, 0.1
endwhile
```

### Contrôle de flux
- `break` : Sort de la boucle actuelle
- `continue` : Passe à l'itération suivante

## Expressions

### Opérateurs arithmétiques
- `+`, `-`, `*`, `/`, `%` (modulo)

### Opérateurs de comparaison
- `==`, `!=`, `<`, `<=`, `>`, `>=`

### Opérateurs logiques
- `and`, `or`, `not`

### Exemples d'expressions
```
$result = 10 + 5 * 2
if, $mouse_x > 100 and $mouse_y < 500
while, $count > 0 and not $stop_flag
```

## Indentation

L'indentation est utilisée pour définir les blocs de code :
```
if, $condition
    echo, Condition vraie
    type, Action
    wait, 1
endif
```

## Commentaires

Les lignes commençant par `#` sont ignorées :
```
# Ceci est un commentaire
$variable = 5  # Commentaire en fin de ligne
```

## Conseils pour la saisie utilisateur

### Bonnes pratiques
1. **Messages clairs** : Utilisez des messages explicites
   ```
   $age = input, "Entrez votre âge (en années)"
   $email = input, "Adresse email (exemple@domain.com)"
   ```

2. **Validation des données** : Vérifiez les valeurs saisies
   ```
   $age = input, "Entrez votre âge"
   if, $age < 0 or $age > 120
       echo, Âge invalide !
   endif
   ```

3. **Valeurs par défaut** : Gérez les annulations
   ```
   $nom = input, "Entrez votre nom"
   if, $nom == ""
       $nom = "Utilisateur"
   endif
   ```

### Gestion des erreurs
- **Annulation** : Si l'utilisateur annule, la variable reçoit une chaîne vide
- **Timeout** : Le système attend maximum 30 secondes par saisie
- **Thread-safe** : Pas de conflit avec l'exécution des macros
- **Logs** : Les saisies sont enregistrées dans la console
