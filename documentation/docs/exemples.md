# Exemples de scripts

## Exemples de base

### Script simple
```
# Script de base - Clic et saisie
echo, Démarrage du script
click, 100, 200, left
wait, 1
type, Bonjour monde
echo, Script terminé
```

### Utilisation des variables
```
# Définition de variables
$message = "Test automatique"
$position_x = 150
$position_y = 250
$delai = 0.5

# Utilisation des variables
echo, $message
click, $position_x, $position_y, left
wait, $delai
type, $message
```

## Saisie utilisateur moderne

### Exemple simple avec input
```
# Saisie utilisateur avec boîtes de dialogue
$nom = input, "Entrez votre nom"
$age = input, "Entrez votre âge"

echo, Bonjour $nom
echo, Vous avez $age ans
type, Nom: $nom, Âge: $age
```

### Formulaire interactif
```
# Formulaire complet avec validation
$nom = input, "Entrez votre nom complet"
$email = input, "Entrez votre adresse email"
$telephone = input, "Entrez votre numéro de téléphone"

# Validation et affichage
if, $nom == ""
    echo, Nom non saisi, utilisation de "Anonyme"
    $nom = "Anonyme"
endif

echo, === Informations saisies ===
echo, Nom: $nom
echo, Email: $email
echo, Téléphone: $telephone

# Remplissage automatique d'un formulaire
click, 200, 150, left
type, $nom
click, 200, 200, left
type, $email
click, 200, 250, left
type, $telephone
```

### Saisie avec calculs
```
# Calculateur interactif
$nombre1 = input, "Entrez le premier nombre"
$nombre2 = input, "Entrez le second nombre"

# Calculs
$somme = $nombre1 + $nombre2
$produit = $nombre1 * $nombre2

echo, $nombre1 + $nombre2 = $somme
echo, $nombre1 × $nombre2 = $produit
```

## Boucles et structures de contrôle

### Boucle simple
```
# Boucle de 5 itérations
$count = 5
loop, $count
    echo, Itération $i sur $count
    type, Ligne $i
    wait, 1
    click, 100, 200, left
endloop
echo, Boucle terminée
```

### Boucle infinie avec arrêt conditionnel
```
# Boucle infinie avec condition d'arrêt
$stop_flag = false
loop, infinite
    echo, Boucle infinie - Itération $i
    wait, 2
    
    # Arrêt après 10 itérations
    if, $i >= 10
        echo, Arrêt de la boucle
        break
    endif
endloop
```

### Conditions if/elseif/else
```
# Test de conditions
$valeur = 15

if, $valeur > 20
    echo, Valeur élevée
    type, Nombre grand
elseif, $valeur > 10
    echo, Valeur moyenne
    type, Nombre moyen
else
    echo, Valeur faible
    type, Nombre petit
endif
```

### Boucle while
```
# Boucle while avec condition
$compteur = 0
while, $compteur < 5
    echo, Compteur: $compteur
    type, Test $compteur
    wait, 1
    $compteur = $compteur + 1
endwhile
echo, Boucle while terminée
```

## Variables système

### Utilisation des variables système
```
# Variables système automatiques
echo, Position souris: $mouse_x, $mouse_y
echo, Résolution écran: $screen_width x $screen_height

# Déplacement relatif
move, $mouse_x + 100, $mouse_y + 50
wait, 1
click, $mouse_x, $mouse_y, left
```

### Boucle avec position de souris
```
# Boucle qui suit la souris
while, $mouse_x < 800
    echo, Position actuelle: $mouse_x, $mouse_y
    click, $mouse_x, $mouse_y, left
    wait, 0.5
    move, $mouse_x + 50, $mouse_y
endwhile
```

## Scripts avancés

### Automatisation de formulaire avec saisie
```
# Formulaire avec saisie interactive
$nom = input, "Nom complet"
$prenom = input, "Prénom"
$email = input, "Adresse email"
$age = input, "Âge"

echo, Remplissage du formulaire pour $prenom $nom

# Remplissage automatique
click, 200, 150, left
wait, 0.5
type, $nom
wait, 0.5

click, 200, 200, left
wait, 0.5
type, $prenom
wait, 0.5

click, 200, 250, left
wait, 0.5
type, $email
wait, 0.5

click, 200, 300, left
wait, 0.5
type, $age

click, 200, 350, left  # Bouton valider
echo, Formulaire rempli pour $prenom $nom
```

### Test de jeu simple
```
# Simulation de clics de jeu
$clics = 10
$delai = 0.2

echo, Démarrage du test de jeu
loop, $clics
    echo, Clic $i sur $clics
    click, 400, 300, left
    wait, $delai
endloop
echo, Test terminé
```

### Script avec input utilisateur avancé
```
# Configuration interactive de macro
$nom_utilisateur = input, "Entrez votre nom d'utilisateur"
$repetitions = input, "Nombre de répétitions (1-100)"
$delai = input, "Délai entre actions (en secondes)"

# Validation des entrées
if, $repetitions == ""
    $repetitions = 5
    echo, Utilisation de 5 répétitions par défaut
endif

if, $delai == ""
    $delai = 1
    echo, Utilisation de 1 seconde par défaut
endif

echo, Configuration:
echo, - Utilisateur: $nom_utilisateur
echo, - Répétitions: $repetitions
echo, - Délai: $delai secondes

# Exécution personnalisée
loop, $repetitions
    echo, Action $i pour $nom_utilisateur
    type, Bonjour $nom_utilisateur - Action $i
    wait, $delai
endloop

echo, Macro terminée pour $nom_utilisateur
```

### Script de test de performance
```
# Test de performance avec mesures
$iterations = input, "Nombre d'itérations pour le test"

if, $iterations == ""
    $iterations = 100
endif

echo, Démarrage du test de performance
echo, Nombre d'itérations: $iterations

loop, $iterations
    if, $i == 0
        echo, Première itération
    elseif, $i == $iterations - 1
        echo, Dernière itération
    endif
    
    click, 100, 100, left
    wait, 0.01
endloop
echo, Test de performance terminé
```

## Scripts utilitaires

### Configuration sauvegarde
```
# Sauvegarde avec configuration
$format = input, "Format de sauvegarde (auto/manuel)"

if, $format == "auto"
    echo, Sauvegarde automatique activée
    hotkey, ctrl+s
    wait, 1
    echo, Sauvegarde automatique terminée
else
    echo, Sauvegarde manuelle
    hotkey, ctrl+shift+s
    wait, 2
    echo, Sauvegarde manuelle terminée
endif
```

### Navigation interactive
```
# Navigation personnalisée
$destination = input, "Où voulez-vous aller? (menu/options/aide)"

if, $destination == "menu"
    echo, Navigation vers le menu
    click, 50, 50, left
elseif, $destination == "options"
    echo, Navigation vers les options
    click, 100, 50, left
elseif, $destination == "aide"
    echo, Navigation vers l'aide
    click, 150, 50, left
else
    echo, Destination inconnue, retour au centre
    move, 400, 300
endif

wait, 1
echo, Navigation terminée
```

### Test personnalisé
```
# Test de réactivité personnalisé
$nb_tests = input, "Nombre de tests à effectuer"
$zone_x = input, "Position X de la zone de test"
$zone_y = input, "Position Y de la zone de test"

if, $nb_tests == ""
    $nb_tests = 5
endif

echo, Test de réactivité personnalisé
echo, Zone: ($zone_x, $zone_y)
echo, Nombre de tests: $nb_tests

loop, $nb_tests
    echo, Test $i/$nb_tests
    click, $zone_x, $zone_y, left
    wait, 0.5
    move, $zone_x + 10, $zone_y + 10
    wait, 0.5
endloop

echo, Test de réactivité terminé
```

## Conseils d'utilisation

### Bonnes pratiques pour input
1. **Messages explicites** : Indiquez clairement ce qui est attendu
   ```
   $age = input, "Entrez votre âge (nombre entre 1 et 120)"
   ```

2. **Gestion des valeurs vides** : Prévoyez des valeurs par défaut
   ```
   $nom = input, "Entrez votre nom"
   if, $nom == ""
       $nom = "Utilisateur"
   endif
   ```

3. **Validation des données** : Vérifiez les entrées utilisateur
   ```
   $nombre = input, "Entrez un nombre"
   if, $nombre < 0
       echo, Erreur: nombre négatif!
   endif
   ```

### Dépannage
- **Boîte de dialogue ne s'affiche pas** : Vérifiez que l'application est au premier plan
- **Valeur vide** : L'utilisateur a annulé ou n'a rien saisi
- **Script qui s'arrête** : Timeout de 30 secondes par saisie
- **Interface bloquée** : Les boîtes de dialogue sont thread-safe et ne bloquent pas l'interface 