# Classe : MacroEngine

Moteur d'exécution des macros avec support des structures de contrôle avancées et interface utilisateur interactive.

## `__init__(gui_callback=None)`

Initialise le moteur avec les contrôleurs clavier et souris et une référence optionnelle vers l'interface GUI.

**Paramètres :**
- `gui_callback` *(MacroGUI)* : Référence vers l'interface graphique pour les interactions utilisateur

**Attributs :**
- `kb` : Contrôleur clavier (`pynput.keyboard.Controller`)
- `ms` : Contrôleur souris (`pynput.mouse.Controller`)
- `stop_event` : Événement d'arrêt (`threading.Event`)
- `pause_event` : Événement de pause (`threading.Event`)
- `gui_callback` : Référence vers l'interface GUI pour les saisies utilisateur

---

## `execute(actions, variables=None, speed=1.0, log_callback=None)`

Exécute une liste d'actions avec support des variables et structures de contrôle.

**Paramètres :**
- `actions` *(list)* : Liste des actions à exécuter (chaînes ou tuples)
- `variables` *(dict)* : Variables définies lors du parsing
- `speed` *(float)* : Facteur de vitesse (0.1 à 5.0)
- `log_callback` *(callable)* : Fonction de log pour les messages

**Fonctionnalités :**
- **Variables dynamiques** : Remplacement en temps réel
- **Structures de contrôle** : Support complet des boucles et conditions
- **Variables système** : Position souris, résolution écran
- **Saisie utilisateur** : Boîtes de dialogue interactives thread-safe
- **Gestion d'erreurs** : Log des erreurs avec callback

---

## `_execute_actions(actions, variables, loop_vars, speed, log_callback)`

Méthode interne qui exécute récursivement les actions avec gestion des structures.

**Paramètres :**
- `actions` *(list)* : Actions à exécuter
- `variables` *(dict)* : Variables globales
- `loop_vars` *(dict)* : Variables de boucle (ex: `$i`)
- `speed` *(float)* : Vitesse d'exécution
- `log_callback` *(callable)* : Fonction de log

**Structures supportées :**
- **LOOP** : Boucles simples et infinies
- **WHILE** : Boucles conditionnelles
- **IF** : Conditions avec elseif/else
- **BREAK/CONTINUE** : Contrôle de flux

---

## `_get_system_vars()`

Retourne les variables système actuelles.

**Retour :**
- `dict` : Variables système
  - `$mouse_x`, `$mouse_y` : Position de la souris
  - `$screen_width`, `$screen_height` : Résolution de l'écran

---

## Commandes supportées

### Clavier
- `press,<touche>,<durée>` : Maintient une touche
- `hotkey,<touches>` : Combinaison de touches
- `type,<texte>` : Saisie de texte

### Souris
- `click,<x>,<y>,<bouton>` : Clic à position
- `lmc/rmc/mmc` : Clics simples
- `move,<x>,<y>` : Déplacement souris
- `scroll,<direction>,<quantité>` : Scroll
- `on/off,<bouton>` : Maintenir/relâcher

### Contrôle
- `wait,<secondes>` : Pause
- `echo,<message>` : Message console

### Saisie utilisateur (nouvelles fonctionnalités)
- `input_var,<variable>,<message>` : **Commande interne** générée par `$var = input,"message"`
- `input,<message>,<variable>` : Ancienne syntaxe supportée

**Fonctionnement de la saisie utilisateur :**
- **Thread-safe** : Utilise la GUI principale via callback
- **Boîtes de dialogue** : Interface moderne avec `tkinter.simpledialog`
- **Timeout** : Maximum 30 secondes par saisie
- **Gestion d'annulation** : Valeur vide si l'utilisateur annule
- **Logs automatiques** : Enregistrement des saisies dans la console

**Exemple d'utilisation :**
```python
# Dans le script macro
$nom = input, "Entrez votre nom"
$age = input, "Entrez votre âge"

# Génère les commandes internes
input_var,$nom,Entrez votre nom
input_var,$age,Entrez votre âge
```

---

## Contrôle d'exécution

### `stop()`
Arrête immédiatement l'exécution de la macro.

### `pause()`
Met en pause l'exécution (peut être reprise).

### `resume()`
Reprend l'exécution après une pause.

---

## Gestion des erreurs

- **Erreurs de syntaxe** : Log avec callback
- **Erreurs d'exécution** : Log et continuation
- **Boucles infinies** : Protection avec limite de sécurité
- **Variables manquantes** : Valeur par défaut 0
- **Erreurs d'input** : Gestion des timeouts et annulations

---

## Sécurité et stabilité

- **Limite de boucles** : Maximum 100 000 itérations pour while
- **Évaluation sécurisée** : Expressions contrôlées
- **Threading sécurisé** : Événements pour arrêt/pause
- **Interface thread-safe** : Saisies utilisateur via GUI principale
- **Gestion mémoire** : Nettoyage automatique des ressources

---

## Integration GUI

### Callback GUI
Le moteur peut être lié à une interface graphique pour :
- **Saisies utilisateur** : Boîtes de dialogue intégrées
- **Logs en temps réel** : Affichage dans la console GUI
- **Contrôles** : Boutons pause/arrêt/reprise
- **Validation** : Vérification syntaxique

### Méthodes GUI requises
Pour une intégration complète, la GUI doit fournir :
- `ask_input(prompt)` : Méthode pour saisie utilisateur thread-safe
- Interface non-bloquante pendant l'exécution
- Gestion des événements système

---

## Exemples d'usage

### Usage basique
```python
engine = MacroEngine()
actions = [('LOOP', 3, ['echo, Test $i', 'wait, 1'])]
engine.execute(actions, {}, 1.0, print)
```

### Usage avec GUI
```python
engine = MacroEngine(gui_callback=my_gui)
actions, variables = parse_script(script_text)
engine.execute(actions, variables, 1.0, my_gui.log_console)
```

### Usage avec saisie utilisateur
```python
# Script contenant: $nom = input, "Votre nom"
actions, variables = parse_script(script_with_input)
# Génère automatiquement les commandes input_var
engine.execute(actions, variables, 1.0, callback)
```
