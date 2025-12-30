# Classe : MacroGUI

Interface graphique Tkinter moderne pour la création et l'exécution de macros avec support de la saisie utilisateur interactive.

## `__init__()`

Initialise l'interface graphique avec tous les composants et le moteur de macros.

**Fenêtre :**
- Titre : "Macro Builder v3.0+ (extended)"
- Taille : 900x700 pixels
- Moteur : Instance de `MacroEngine` avec callback GUI

**Integration moteur :**
```python
self.engine = MacroEngine(gui_callback=self)
```

---

## `_build_ui()`

Crée l'interface utilisateur complète.

### Barre de menu
- **Fichier** : Ouvrir, Enregistrer
- **Édition** : Valider Syntaxe
- **Aide** : À propos

### Composants principaux
- **Zone de script** : Éditeur de texte pour le script macro
- **Console** : Affichage des logs en temps réel (fond noir, texte vert)
- **Contrôles** : Vitesse, Exécuter, Pause, Arrêter

---

## Méthodes de contrôle

### `log_console(msg)`
Ajoute un message horodaté à la console.

**Paramètres :**
- `msg` *(str)* : Message à afficher

**Fonctionnalités :**
- Horodatage automatique
- Auto-scroll vers le bas
- Thread-safe pour les logs depuis les macros

### `load_file()`
Ouvre un fichier de script (.txt) et le charge dans l'éditeur.

### `save_file()`
Sauvegarde le script actuel dans un fichier (.txt).

### `validate_syntax()`
Vérifie la syntaxe du script et affiche le résultat.

**Fonctionnalités :**
- Parsing complet du script
- Détection des erreurs de syntaxe
- Message d'information ou d'erreur

---

## Contrôle d'exécution

### `start_macro()`
Démarre l'exécution de la macro dans un thread séparé.

**Processus :**
1. Parse le script avec `parse_script()`
2. Vide la console
3. Lance l'exécution en arrière-plan
4. Gère les erreurs de syntaxe

### `stop_macro()`
Arrête immédiatement l'exécution de la macro.

### `pause_macro()`
Met en pause ou reprend l'exécution.

**Fonctionnalités :**
- Bascule entre pause et reprise
- Log des changements d'état
- Interface réactive

---

## Saisie utilisateur (nouvelle fonctionnalité)

### `ask_input(prompt)`
**Méthode thread-safe pour demander une saisie utilisateur via boîte de dialogue.**

**Paramètres :**
- `prompt` *(str)* : Message à afficher à l'utilisateur

**Retour :**
- `str` : Valeur saisie par l'utilisateur (chaîne vide si annulé)

**Fonctionnement :**
- **Thread-safe** : Utilise `self.after()` pour exécuter dans le thread principal
- **Interface moderne** : Boîte de dialogue `tkinter.simpledialog`
- **Parent correct** : Liée à la fenêtre principale (`parent=self`)
- **Timeout** : Attente maximum 30 secondes
- **Gestion d'erreurs** : Log automatique des erreurs

**Exemple d'usage interne :**
```python
# Appelé automatiquement par le moteur pour $nom = input, "Votre nom"
result = gui.ask_input("Votre nom")
```

**Processus d'exécution :**
1. Planification via `self.after(0, do_ask)`
2. Création de la boîte de dialogue dans le thread principal
3. Attente de la saisie utilisateur avec boucle non-bloquante
4. Retour de la valeur ou chaîne vide si timeout/annulation

---

## Interface utilisateur

### Zone de script
- **Éditeur de texte** : Saisie du script macro
- **Support complet** : Syntaxe colorée (si disponible)
- **Taille** : Hauteur de 22 lignes

### Console de logs
- **Style** : Fond noir (#222), texte vert (#0f0)
- **Police** : Consolas 10pt
- **Fonctionnalités** : Auto-scroll, horodatage
- **État** : Lecture seule pendant l'exécution

### Contrôles de vitesse
- **Slider** : Vitesse de 0.1x à 5.0x
- **Valeur par défaut** : 1.0x

### Boutons d'action
- **▶ Exécuter** : Démarre la macro
- **⏸ Pause** : Pause/Reprise
- **⏹ Arrêter** : Arrêt immédiat

---

## Gestion des erreurs

- **Erreurs de syntaxe** : Boîte de dialogue d'erreur
- **Erreurs d'exécution** : Log dans la console
- **Fichiers** : Gestion des erreurs d'ouverture/sauvegarde
- **Input timeout** : Gestion automatique des timeouts de saisie
- **Threading** : Protection contre les erreurs de concurrence

---

## Threading et sécurité

### Exécution des macros
- **Thread séparé** : Les macros s'exécutent en arrière-plan
- **Interface réactive** : Pas de blocage de l'UI
- **Contrôles** : Communication via événements (`threading.Event`)

### Saisie utilisateur thread-safe
- **Mécanisme** : `self.after()` pour exécution dans le thread principal
- **Boucle d'attente** : Non-bloquante avec `self.update()`
- **Timeout** : Protection contre les blocages infinis
- **Ressources** : Nettoyage automatique des boîtes de dialogue

---

## Fonctionnalités avancées

### Validation syntaxique
- **Parsing complet** : Vérification de toutes les structures
- **Messages détaillés** : Information précise sur les erreurs
- **Validation des variables** : Contrôle des expressions

### Interface moderne
- **Design épuré** : Layout professionnel
- **Logs colorés** : Console style terminal
- **Contrôles intuitifs** : Boutons avec icônes Unicode

### Integration avec le moteur
- **Callback GUI** : Référence bidirectionnelle
- **Logs en temps réel** : Affichage immédiat des messages
- **Saisies interactives** : Boîtes de dialogue intégrées
- **Contrôle total** : Pause, arrêt, reprise depuis l'interface

---

## Exemple d'utilisation

### Création de l'interface
```python
app = MacroGUI()
# Moteur automatiquement créé avec callback
# self.engine = MacroEngine(gui_callback=self)
```

### Script avec saisie utilisateur
```
# Dans l'éditeur de script
$nom = input, "Entrez votre nom"
$age = input, "Entrez votre âge"
echo, Bonjour $nom, vous avez $age ans
```

### Exécution
1. L'utilisateur clique "▶ Exécuter"
2. Des boîtes de dialogue apparaissent pour les saisies
3. Les logs s'affichent en temps réel dans la console
4. L'interface reste réactive pendant l'exécution 
    