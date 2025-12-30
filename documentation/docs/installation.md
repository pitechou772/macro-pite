# Installation

## Prérequis

### Système
- **Système d'exploitation** : Windows, macOS, ou Linux
- **Python** : Version 3.8 ou plus récente
- **Permissions** : Accès aux entrées clavier et souris (nécessaire pour l'automatisation)

### Dépendances Python
```bash
pip install pynput
pip install tkinter  # Généralement inclus avec Python
```

## Installation

### Méthode 1 : Installation directe
1. **Télécharger** le code source du projet
2. **Extraire** les fichiers dans un dossier
3. **Ouvrir un terminal** dans le dossier du projet
4. **Installer les dépendances** :
   ```bash
   pip install pynput
   ```
5. **Lancer l'application** :
   ```bash
   python main.py
   ```

### Méthode 2 : Clonage depuis Git
```bash
git clone https://github.com/pite772/macro-builder.git
cd macro-builder
pip install pynput
python main.py
```

## Vérification de l'installation

### Test rapide
1. Lancez l'application avec `python main.py`
2. Une fenêtre "Macro Builder v3.0+ (extended)" devrait s'ouvrir
3. Testez un script simple :
   ```
   echo, Test d'installation
   wait, 1
   echo, Installation réussie
   ```

### Test complet
Créez un fichier de test `test.txt` :
```
# Test complet de l'installation
$count = 3
echo, Démarrage du test
loop, $count
    echo, Itération $i
    wait, 0.5
endloop
echo, Test terminé avec succès
```

## Dépannage

### Erreurs courantes

#### ModuleNotFoundError: No module named 'pynput'
```bash
pip install pynput
```

#### Permission denied (Linux/macOS)
Sur Linux ou macOS, vous pourriez avoir besoin de permissions spéciales :
```bash
sudo python main.py
```

#### Erreur de permissions Windows
- Exécutez en tant qu'administrateur
- Vérifiez les paramètres de sécurité Windows

#### Interface graphique ne s'affiche pas
Vérifiez que tkinter est installé :
```bash
python -c "import tkinter; print('tkinter OK')"
```

### Support des systèmes

#### Windows
- **Compatible** : Windows 10, 11
- **Permissions** : Peut nécessiter l'exécution en tant qu'administrateur
- **Antivirus** : Certains antivirus peuvent bloquer l'automatisation

#### macOS
- **Compatible** : macOS 10.14+
- **Permissions** : Accorder l'accès aux entrées dans Préférences Système
- **Sécurité** : Peut nécessiter des autorisations spéciales

#### Linux
- **Compatible** : Distributions récentes
- **Permissions** : Peut nécessiter sudo pour l'accès aux entrées
- **Environnement** : Fonctionne avec la plupart des gestionnaires de fenêtres

## Configuration avancée

### Variables d'environnement
```bash
# Désactiver les logs de debug
export PYNPUT_LOG_LEVEL=ERROR

# Spécifier le backend (Linux)
export DISPLAY=:0
```

### Fichier de configuration
L'application utilise des paramètres par défaut, mais vous pouvez créer un fichier de configuration personnalisé si nécessaire.

## Mise à jour

### Mise à jour du code
```bash
git pull origin main
```

### Mise à jour des dépendances
```bash
pip install --upgrade pynput
```

## Support

En cas de problème :
1. Vérifiez les prérequis
2. Consultez la section dépannage
3. Vérifiez les logs de l'application
4. Consultez la documentation des modules


