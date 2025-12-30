# Macro Builder v3.0+ (extended)

Outil Python avec interface graphique permettant de créer et exécuter des macros clavier/souris à partir de scripts textuels avec support avancé des structures de contrôle et saisie utilisateur interactive.

## Fonctionnalités principales
- **Scripts avancés** : Variables, boucles, conditions (if/elseif/else), boucles while
- **Structures de contrôle** : `if/elseif/else/endif`, `while/endwhile`, `loop/endloop`, `break/continue`
- **Variables système** : `$mouse_x`, `$mouse_y`, `$screen_width`, `$screen_height`
- **Variables de boucle** : `$i` (index de boucle)
- **Saisie utilisateur** : Boîtes de dialogue interactives thread-safe avec `$var = input,"message"`
- **Expressions sécurisées** : Support des opérations arithmétiques, comparaisons et logiques
- **Automatisation complète** : Clavier et souris via `pynput`
- **Interface moderne** : Tkinter avec console intégrée et contrôles de vitesse
- **Validation syntaxique** : Vérification des scripts avant exécution

## Nouvelles fonctionnalités v3.0+
- **Conditions avancées** : Support complet des structures if/elseif/else
- **Boucles while** : Exécution conditionnelle avec sécurité intégrée
- **Variables dynamiques** : Évaluation en temps réel avec variables système
- **Expressions complexes** : Support des opérateurs logiques (and, or, not)
- **Saisie utilisateur moderne** : Interface intuitive avec `$variable = input,"message"`
- **Threading sécurisé** : Boîtes de dialogue thread-safe sans blocage de l'interface
- **Sécurité renforcée** : Évaluation sécurisée des expressions
- **Interface améliorée** : Contrôles de pause/reprise et validation syntaxique

## Exemples d'utilisation

### Script avec saisie utilisateur
```
# Configuration interactive
$nom = input, "Entrez votre nom"
$repetitions = input, "Nombre de répétitions"

# Exécution personnalisée
echo, Bonjour $nom
loop, $repetitions
    echo, Action $i pour $nom
    type, Test automatisé
    wait, 1
endloop
```

### Automatisation intelligente
```
# Variables système et conditions
if, $mouse_x > $screen_width / 2
    echo, Souris à droite de l'écran
    click, 100, 100, left
else
    echo, Souris à gauche de l'écran
    click, 500, 100, left
endif
```

---
