# FIITECH
FIITECH SOLUTIONS
API Endpoints attendus :
GET /api/services/ - Liste des services actifs

GET /api/projects/ - Liste de tous les projets

GET /api/testimonials/ - Liste des témoignages approuvés

Interface d'administration :
Personnalisation de l'interface Django Admin

Filtres et recherches sur les modèles


# INSTALLATION
Cloner le projet:
git clone https://github.com/bass2-3/FIITECH.git
cd FIITECH

## **Créer un environnement virtuel**
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

## **Installer les dépendances**
pip install django djangorestframework pillow

## **Configuration Initiale:**
### **Créer et appliquer les migrations**
python manage.py makemigrations
python manage.py migrate

### **Créer un superutilisateur**
python manage.py createsuperuser

### **Collecter les fichiers statiques**
python manage.py collectstatic

### **Lancer le serveur**
python manage.py runserver

