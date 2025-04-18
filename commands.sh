# Créer le dossier static/images
mkdir -p static/images

# Déplacer les logos vers le dossier static/images
mv geostrat-logo.png static/images/
mv pass-drc-logo.png static/images/

# Donner les bonnes permissions aux fichiers
chmod 644 static/images/*.png
chmod 755 static/images


