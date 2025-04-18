from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os

app = Flask(__name__, static_folder='static')

# Configuration de la base de données
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre_clé_secrète_ici')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///survey.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Route pour servir les fichiers statiques
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

# Liste des pays africains
AFRICAN_COUNTRIES = [
    'Afrique du Sud', 'Algérie', 'Angola', 'Bénin', 'Botswana', 'Burkina Faso', 
    'Burundi', 'Cameroun', 'Cap-Vert', 'Comores', 'Congo', 'Côte d\'Ivoire', 
    'Djibouti', 'Égypte', 'Érythrée', 'Éthiopie', 'Gabon', 'Gambie', 'Ghana', 
    'Guinée', 'Guinée-Bissau', 'Guinée équatoriale', 'Kenya', 'Lesotho', 'Libéria',
    'Libye', 'Madagascar', 'Malawi', 'Mali', 'Maroc', 'Maurice', 'Mauritanie',
    'Mozambique', 'Namibie', 'Niger', 'Nigeria', 'Ouganda', 'Rwanda', 'Republique démocratique du Congo',
    'Sao Tomé-et-Principe', 'Sénégal', 'Seychelles', 'Sierra Leone', 'Somalie',
    'Soudan', 'Soudan du Sud', 'Swaziland', 'Tanzanie', 'Tchad', 'Togo', 
    'Tunisie', 'Zambie', 'Zimbabwe'
]

class Survey(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Section 1: Profil du répondant
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    country = db.Column(db.String(100))
    company_name = db.Column(db.String(200))
    sector = db.Column(db.String(100))
    function = db.Column(db.String(100))
    experience_duration = db.Column(db.String(50))
    
    # Section 2: Informations sur l'entreprise
    company_type = db.Column(db.String(50))
    spatial_data_types = db.Column(db.String(500))
    application_domains = db.Column(db.String(500))
    data_sources = db.Column(db.String(500))
    annual_budget = db.Column(db.String(50))
    software_tools = db.Column(db.String(500))
    employee_training = db.Column(db.String(50))
    
    # Section 3: Impact et défis
    benefits = db.Column(db.String(500))
    obstacles = db.Column(db.String(500))
    success_story = db.Column(db.Text)
    success_metrics = db.Column(db.Text)
    local_partners = db.Column(db.String(500))
    data_quality_management = db.Column(db.String(100))
    local_adaptation = db.Column(db.Text)
    
    # Section 4: Besoins et perspectives
    desired_support = db.Column(db.String(500))
    future_plans = db.Column(db.String(100))
    recommendations = db.Column(db.Text)
    internet_access = db.Column(db.String(50))
    free_data_impact = db.Column(db.String(100))
    
    # Section 5: Innovation
    ai_ml_usage = db.Column(db.String(100))
    low_cost_solutions = db.Column(db.Text)
    tool_customization = db.Column(db.String(100))
    solution_replication = db.Column(db.String(100))
    
    # Nouveaux champs
    data_frequency = db.Column(db.String(50))
    data_storage = db.Column(db.String(50))
    data_sharing = db.Column(db.String(50))
    mobile_usage = db.Column(db.String(50))
    local_expertise = db.Column(db.String(50))
    blockchain_usage = db.Column(db.String(50))
    organization_type = db.Column(db.String(50))
    years_experience = db.Column(db.String(20))
    data_types = db.Column(db.String(500))
    data_volume = db.Column(db.String(50))
    training_needs = db.Column(db.String(500))
    funding_source = db.Column(db.String(500))
    annual_spatial_budget = db.Column(db.String(50))
    main_challenges = db.Column(db.String(500))
    future_priorities = db.Column(db.Text)
    
    # Ajouter les champs de géolocalisation
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Vérification que tous les champs requis sont présents
        required_fields = [
            'name', 'email', 'country', 'company_name', 'sector',
            'organization_type', 'application_domains', 'software_tools',
            'benefits', 'obstacles', 'success_story',
            # Ajoutez tous vos champs requis ici
        ]
        
        for field in required_fields:
            if not request.form.get(field):
                flash('Tous les champs marqués d\'un astérisque (*) sont obligatoires.', 'error')
                return redirect(url_for('survey'))
        
        # Si tous les champs sont valides, continuez avec la création de l'enquête
        survey_id = str(uuid.uuid4())
        new_survey = Survey(
            id=survey_id,
            name=request.form.get('name'),
            email=request.form.get('email'),
            country=request.form.get('country'),
            # ... autres champs ...
        )
        
        try:
            db.session.add(new_survey)
            db.session.commit()
            flash('Merci pour votre participation!', 'success')
            return redirect(url_for('thank_you'))
        except Exception as e:
            db.session.rollback()
            flash('Une erreur est survenue lors de l\'enregistrement de votre réponse.', 'error')
            return redirect(url_for('survey'))
            
    return render_template('survey.html', countries=AFRICAN_COUNTRIES)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/map')
def view_map():
    # Récupérer toutes les réponses avec des coordonnées valides
    responses = Survey.query.filter(
        Survey.latitude.isnot(None),
        Survey.longitude.isnot(None)
    ).all()
    
    return render_template('map.html', responses=responses)

@app.route('/healthz')
def health_check():
    try:
        # Test la connexion à la base de données
        db.session.execute('SELECT 1')
        return 'OK', 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)





