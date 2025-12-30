

# 📘 Macro Builder v4.0 — Spécification Technique Complète

> Ce document décrit précisément l’architecture, le langage, le comportement et les règles internes de Macro Builder v4.0.
> Il permet à un développeur de recréer entièrement le projet sans accès au code original.

---

## 1. Objectif du projet

Macro Builder est une application desktop permettant :

* de créer des macros clavier et souris
* via un langage de script dédié (DSL)
* avec une interface graphique
* et un moteur d’exécution contrôlable (pause, stop, debug)

Le projet vise :

* la lisibilité
* la sécurité
* l’extensibilité (v3 → v4+)

---

## 2. Stack technique imposée

### Langage

* Python 3.10+

### Bibliothèques principales

* `tkinter` : interface graphique
* `pynput` : contrôle clavier et souris
* `time` : gestion des délais
* `threading` : exécution non bloquante
* `json` : import/export
* (optionnel) `PIL` / `opencv-python` : détection pixel/image

---

## 3. Architecture générale

```
macro_builder/
│
├── main.py                 # Point d’entrée
├── ui/
│   ├── window.py           # Fenêtre principale
│   ├── editor.py           # Zone d’édition + lignes
│   ├── controls.py         # Boutons, sliders, logs
│
├── engine/
│   ├── parser.py           # Analyse du script
│   ├── executor.py         # Exécution ligne par ligne
│   ├── context.py          # Variables, état global
│   ├── recorder.py         # Enregistrement actions
│
├── commands/
│   ├── keyboard.py
│   ├── mouse.py
│   ├── control.py
│
├── utils/
│   ├── file_io.py
│   ├── color.py
│   ├── logger.py
│
└── assets/
```

---

## 4. Modèle d’exécution

### Principe

* Le script est lu **ligne par ligne**
* Chaque ligne devient une **Instruction**
* L’exécution se fait dans un **thread séparé**
* Le moteur doit supporter :

  * pause
  * reprise
  * arrêt immédiat

---

## 5. Règles du langage (DSL v4)

### 5.1 Syntaxe générale

* Une instruction par ligne
* Séparateur : `,`
* Indentation = structure logique
* Commentaire : `#`

---

### 5.2 Variables

#### Déclaration

```
$nom = "Jean"
$age = 25
```

#### Types

* string
* int
* float
* bool

#### Calculs

```
$score += 10
$hp -= 1
```

---

### 5.3 Variables automatiques

| Nom           | Description        |
| ------------- | ------------------ |
| `$i`          | Compteur de boucle |
| `@speed`      | Vitesse globale    |
| `@iterations` | Variable UI        |

---

## 6. Boucles

### Boucle simple

```
loop,5
    ...
next
```

### Boucle infinie

```
loop,infinite
    ...
endloop
```

### Boucle conditionnelle

```
while,$hp > 0
    ...
endwhile
```

---

## 7. Conditions

### Syntaxe

```
if,condition
    ...
endif
```

### Conditions supportées

* `$a == $b`
* `$a != 10`
* `$x > 5`
* `exists,$var`
* `pixel,x,y,#RRGGBB`

---

## 8. Fonctions

### Déclaration

```
function heal()
    press,h,0.1
endfunction
```

### Appel

```
heal()
```

Les fonctions :

* n’ont pas de retour
* ont accès au contexte global

---

## 9. Commandes clavier

| Commande             | Effet        |
| -------------------- | ------------ |
| `press,touche,durée` | Appui simple |
| `press,ctrl+c,durée` | Combo        |
| `hotkey,alt+tab`     | Raccourci    |
| `type,texte`         | Écriture     |

Touches spéciales mappées via `pynput.keyboard.Key`.

---

## 10. Commandes souris

| Commande              | Effet          |
| --------------------- | -------------- |
| `lmc` / `rmc` / `mmc` | Click          |
| `move,x,y`            | Déplacement    |
| `click,x,y,left`      | Click position |
| `drag,x1,y1,x2,y2`    | Glisser        |
| `scroll,up,3`         | Scroll         |
| `on,lmc` / `off,lmc`  | Maintien       |

---

## 11. Commandes de contrôle

| Commande        | Description |
| --------------- | ----------- |
| `wait,secondes` | Pause       |
| `echo,message`  | Log         |
| `breakpoint`    | Pause debug |

---

## 12. Enregistrement automatique

### Fonctionnement

* Capture :

  * touches pressées
  * clicks
  * positions
  * délais
* Génère un script DSL équivalent
* Nettoyage automatique (groupes, délais inutiles)

---

## 13. Mode Debug

Fonctionnalités obligatoires :

* Ligne active surlignée
* Valeurs des variables affichées
* Step by step
* Breakpoints

---

## 14. Import / Export

### Format JSON

```json
{
  "version": "4.0",
  "speed": 1.2,
  "script": "...",
  "metadata": {
    "created_at": "ISO-8601"
  }
}
```

---

## 15. Sécurité

* Limite d’itérations configurable
* Timeout global
* Bouton STOP toujours prioritaire
* Blocage des `eval()` dangereux

---

## 16. Règles non négociables

* Le moteur ne doit jamais bloquer l’UI
* Un script invalide ne s’exécute jamais
* Toute boucle infinie doit contenir un `wait`
* L’arrêt utilisateur doit être immédiat

---

## 17. Résultat attendu

Un développeur recevant **uniquement ce document** doit pouvoir :

* recréer l’UI
* implémenter le parser
* reconstruire le moteur
* reproduire le comportement exact

---

## 18. Statut

Version de référence : **Macro Builder v4.0**
Document : **Spécification officielle**

---


