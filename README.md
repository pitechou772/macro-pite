# 🚀 Macro Builder v3.0 - Guide Complet

Un outil d'automatisation puissant pour créer et exécuter des macros avancées avec boucles imbriquées, variables et enregistrement automatique.

## 📋 Table des Matières

- [Installation](#installation)
- [Démarrage Rapide](#démarrage-rapide)
- [Syntaxe des Commandes](#syntaxe-des-commandes)
- [Boucles et Structures](#boucles-et-structures)
- [Variables](#variables)
- [Interface Utilisateur](#interface-utilisateur)
- [Exemples Pratiques](#exemples-pratiques)
- [Fonctionnalités Avancées](#fonctionnalités-avancées)
- [Dépannage](#dépannage)

## 🔧 Installation

### Prérequis
```bash
pip install tkinter pynput
```

### Lancement
```bash
python macro_builder_v3.py
```

## ⚡ Démarrage Rapide

1. **Lancez l'application**
2. **Écrivez votre script** dans la zone de texte (gauche)
3. **Ajustez la vitesse** avec le curseur (droite)
4. **Cliquez sur "▶ Exécuter"**

### Premier Script
```
type,Bonjour le monde!
press,enter,0.1
wait,1.0
type,Ma première macro
```

## 📖 Syntaxe des Commandes

### 🎹 Commandes Clavier

| Commande | Syntaxe | Description | Exemple |
|----------|---------|-------------|---------|
| `press` | `press,touche,durée` | Appuyer sur une touche | `press,a,0.1` |
| `press` | `press,combo,durée` | Combinaison de touches | `press,ctrl+c,0.5` |
| `hotkey` | `hotkey,combo` | Raccourci rapide | `hotkey,alt+tab` |
| `type` | `type,texte` | Taper du texte | `type,Hello World` |

**Touches spéciales disponibles :**
- `enter`, `space`, `tab`, `backspace`, `delete`
- `ctrl`, `alt`, `shift`, `esc`, `home`, `end`
- `up`, `down`, `left`, `right`
- `f1` à `f12`

### 🖱️ Commandes Souris

| Commande | Syntaxe | Description | Exemple |
|----------|---------|-------------|---------|
| `lmc` | `lmc` | Click gauche | `lmc` |
| `rmc` | `rmc` | Click droit | `rmc` |
| `mmc` | `mmc` | Click milieu | `mmc` |
| `click` | `click,x,y,bouton` | Click à position | `click,100,200,left` |
| `drag` | `drag,x1,y1,x2,y2` | Glisser-déposer | `drag,0,0,100,100` |
| `move` | `move,x,y` | Déplacer curseur | `move,500,300` |
| `scroll` | `scroll,direction,quantité` | Défiler | `scroll,up,3` |
| `on` | `on,bouton` | Maintenir enfoncé | `on,lmc` |
| `off` | `off,bouton` | Relâcher | `off,lmc` |

### ⏱️ Commandes de Contrôle

| Commande | Syntaxe | Description | Exemple |
|----------|---------|-------------|---------|
| `wait` | `wait,secondes` | Attendre | `wait,2.5` |
| `echo` | `echo,message` | Message debug | `echo,Debug info` |

## 🔄 Boucles et Structures

### Boucles Simples
```
loop,5
    type,Répétition numéro $i
    press,enter,0.1
    wait,0.5
next
```

### Boucles Imbriquées
```
loop,3
    type,Boucle externe $i
    press,enter,0.1
    
    loop,2
        type,  Boucle interne $i
        press,tab,0.1
    next
    
    wait,1.0
next
```

### Boucle Infinie
```
loop,infinite
    type,Boucle sans fin
    wait,1.0
    # Utilisez le bouton "Arrêter" pour stopper
endloop
```

### Conditions
```
if,true
    type,Cette condition est vraie
    press,enter,0.1
endif
```

**⚠️ Important :** L'indentation (espaces ou tabulations) définit l'imbrication des blocs !

## 📊 Variables

### Définir des Variables
```
$nom = Jean Dupont
$age = 25
$email = jean@example.com
```

### Utiliser des Variables
```
type,Nom: $nom
press,tab,0.1
type,Age: $age
press,tab,0.1
type,Email: $email
```

### Variables Automatiques
- `$i` : Compteur de boucle automatique (commence à 0)

```
loop,5
    type,Itération numéro $i
    press,enter,0.1
next
```

## 🖥️ Interface Utilisateur

### Zone d'Édition (Gauche)
- **Éditeur de texte** avec coloration syntaxique
- **Numérotation des lignes** automatique
- **Support de l'indentation** pour les boucles

### Panneau de Contrôle (Droite)

#### Exécution
- **Curseur de vitesse** : 0.1x à 5.0x
- **▶ Exécuter** : Lancer la macro
- **⏸ Pause** : Suspendre/reprendre
- **⏹ Arrêter** : Arrêt immédiat

#### Enregistrement
- **🔴 Enregistrer** : Capturer vos actions automatiquement
- Génère le script correspondant

#### Status
- **Log en temps réel** avec timestamps
- **Barre de progression** détaillée
- **Messages d'erreur** explicites

### Menu Principal

#### Fichier
- **Nouveau** (Ctrl+N) : Script vierge
- **Ouvrir** (Ctrl+O) : Charger fichier .macro/.txt
- **Enregistrer** (Ctrl+S) : Sauvegarder
- **Import/Export JSON** : Avec métadonnées

#### Édition
- **Insérer Template** : Modèles prêts à l'emploi
- **Valider Syntaxe** : Vérification avant exécution

#### Aide
- **Syntaxe** : Guide complet
- **À propos** : Informations version

## 💡 Exemples Pratiques

### 1. Automatisation de Saisie
```
# Remplir un formulaire
$prenom = Marie
$nom = Martin
$tel = 0123456789

type,$prenom
press,tab,0.1
type,$nom
press,tab,0.1  
type,$tel
press,enter,0.5
```

### 2. Navigation Web
```
# Ouvrir plusieurs onglets
loop,5
    hotkey,ctrl+t
    wait,0.5
    type,https://example$i.com
    press,enter,1.0
next
```

### 3. Test de Performance
```
# Stress test avec timing
$iterations = 100
loop,$iterations
    echo,Test $i/$iterations
    hotkey,ctrl+r
    wait,2.0
    press,esc,0.1
next
```

### 4. Automation Gaming
```
# Macro de jeu avec combos
wait,5
loop,infinite
    on,lmc
    loop,27
        press,d+z,15
        press,z,2
        press,q+z,15
        press,z,2
    endloop
    off,lmc
    type,!warp garden
endloop
```

### 5. Nettoyage de Fichiers
```
# Sélectionner et supprimer
loop,10
    press,down,0.1
    press,shift+down,0.1
next
press,delete,0.5
press,enter,0.1  # Confirmer
```

## 🎯 Fonctionnalités Avancées

### Enregistrement Automatique
1. Cliquez **🔴 Enregistrer**
2. Effectuez vos actions (clavier + souris)
3. Cliquez **⏹ Arrêter Rec**
4. Le script est généré automatiquement

### Templates Intégrés
- **Test de frappe** : Saisie automatique
- **Navigation fenêtres** : Alt+Tab automation
- **Remplissage formulaires** : Données structurées
- **Macros gaming** : Séquences répétitives
- **Automation clicks** : Positionnement précis

### Contrôles Avancés

#### Vitesse Variable
- **0.1x** : Ultra lent (debug)
- **1.0x** : Vitesse normale
- **5.0x** : Ultra rapide

#### Pause/Reprise
- Suspendre à tout moment
- Reprendre exactement où arrêté
- État sauvegardé

#### Arrêt d'Urgence
- Bouton **⏹ Arrêter** toujours accessible
- Arrêt immédiat et sécurisé

### Import/Export JSON
```json
{
  "script": "type,Hello\nwait,1.0",
  "speed": 1.5,
  "exported_at": "2024-01-15T10:30:00"
}
```

## 🐞 Dépannage

### Problèmes Courants

#### "Erreur de syntaxe"
- ✅ Vérifiez l'indentation (espaces/tabs cohérents)
- ✅ Validez que chaque `loop` a son `next`
- ✅ Utilisez la fonction **Valider Syntaxe**

#### "Macro ne s'exécute pas"
- ✅ Vérifiez les permissions (certaines apps bloquent l'automation)
- ✅ Testez avec un script simple d'abord
- ✅ Regardez les logs de status

#### "Actions trop rapides/lentes"
- ✅ Ajustez le curseur de vitesse
- ✅ Ajoutez des `wait` entre actions critiques
- ✅ Utilisez la pause pour débugger

#### "Variables non reconnues"
- ✅ Définissez avec `$nom = valeur` avant usage
- ✅ Utilisez exactement le même nom
- ✅ Pas d'espaces dans les noms de variables

### Messages d'Erreur

| Message | Cause | Solution |
|---------|-------|----------|
| `Invalid loop count` | Compteur de boucle invalide | Utilisez un nombre entier |
| `Loop nécessite un paramètre` | `loop` sans nombre | Ajoutez `,10` par exemple |
| `Condition non reconnue` | Syntaxe if incorrecte | Utilisez `if,true` pour test |

### Performance

#### Scripts Lents
- Réduisez les `wait` inutiles
- Augmentez la vitesse d'exécution
- Optimisez les boucles imbriquées

#### Utilisation Mémoire
- Évitez les boucles infinies sans `wait`
- Limitez les boucles à 10000 itérations max
- Nettoyez les logs régulièrement

## 🔒 Sécurité et Bonnes Pratiques

### Recommandations
- ✅ **Testez d'abord** avec vitesse lente (0.1x)
- ✅ **Sauvegardez** vos scripts importants
- ✅ **Utilisez des wait** pour éviter les blocages
- ✅ **Préparez un arrêt d'urgence** (bouton Stop)

### Limites
- ⚠️ Certaines applications bloquent l'automation
- ⚠️ Les boucles infinies peuvent surcharger le système
- ⚠️ Permissions administrateur parfois nécessaires

## 📞 Support

### Résolution de Problèmes
1. Consultez les **logs de status** (panneau droit)
2. Utilisez **Valider Syntaxe** avant exécution
3. Testez avec des scripts simples d'abord
4. Vérifiez la **syntaxe d'indentation**

### Ressources
- **Menu Aide > Syntaxe** : Reference complète
- **Templates intégrés** : Exemples fonctionnels
- **Mode debug** : Vitesse 0.1x + echo messages

---

## 🎉 Conclusion

Macro Builder v3.0 est un outil puissant pour automatiser vos tâches répétitives. Avec ses boucles imbriquées, variables et interface moderne, vous pouvez créer des automatisations sophistiquées en quelques minutes.

**Bon scripting ! 🚀**

---

*Version 3.0 - Dernière mise à jour : 2024*