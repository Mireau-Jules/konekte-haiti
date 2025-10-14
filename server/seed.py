#!/usr/bin/env python3

from app import app
from models import db, User, ServiceProvider, Review
from datetime import datetime

def seed_data():
    with app.app_context():
        # Delete existing data
        print("Deleting existing data...")
        Review.query.delete()
        ServiceProvider.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("Creating users...")
        # Create Users
        users = [
            User(name="Marie Jean-Baptiste", email="marie.jb@email.ht"),
            User(name="Pierre Louis", email="pierre.louis@email.ht"),
            User(name="Claudette Estimé", email="claudette.estime@email.ht"),
            User(name="Jean-Robert Dupont", email="jeanrobert.d@email.ht"),
            User(name="Micheline Pierre", email="micheline.p@email.ht"),
            User(name="Jacques Morisseau", email="jacques.m@email.ht"),
        ]
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        print("Creating service providers...")
        # Create Service Providers
        
        # Medical/Health Services
        medical_services = [
            ServiceProvider(
                name="Hôpital Général de Port-au-Prince",
                category="Medical/Health",
                description="Hôpital public offrant des services médicaux généraux, urgences 24/7, et soins spécialisés. Personnel médical qualifié disponible.",
                location="Boulevard Jean-Jacques Dessalines, Port-au-Prince",
                phone="2222-2323",
                hours="24/7 - Urgences disponibles",
                user_id=users[0].id
            ),
            ServiceProvider(
                name="Clinique Médico-Sociale de Delmas",
                category="Medical/Health",
                description="Clinique communautaire offrant consultations, vaccinations, soins prénataux et services de laboratoire à prix abordables.",
                location="Delmas 33, près du marché",
                phone="3456-7890",
                hours="Lundi-Vendredi: 7h-17h, Samedi: 8h-14h",
                user_id=users[1].id
            ),
            ServiceProvider(
                name="Pharmacie Solidarité",
                category="Medical/Health",
                description="Pharmacie communautaire avec médicaments génériques abordables. Personnel formé pour conseils pharmaceutiques.",
                location="Route de Frères, Pétion-Ville",
                phone="2811-4455",
                hours="Lundi-Samedi: 8h-19h, Dimanche: 9h-13h",
                user_id=users[0].id
            ),
        ]
        
        # Education Services
        education_services = [
            ServiceProvider(
                name="Bibliothèque Communautaire Dessalines",
                category="Education",
                description="Bibliothèque publique avec livres en français et créole, accès internet gratuit, et espace d'étude silencieux pour étudiants.",
                location="Rue Capois, près de la Place Boyer",
                phone="2234-5566",
                hours="Lundi-Vendredi: 8h-18h, Samedi: 9h-15h",
                user_id=users[2].id
            ),
            ServiceProvider(
                name="École Nationale de Carrefour",
                category="Education",
                description="École publique primaire et secondaire accueillant 800 élèves. Programmes en français et créole avec activités parascolaires.",
                location="Carrefour, Route de l'Aéroport",
                phone="3877-9988",
                hours="Lundi-Vendredi: 7h-15h",
                user_id=users[2].id
            ),
            ServiceProvider(
                name="Centre de Formation Professionnelle",
                category="Education",
                description="Formation en informatique, couture, électricité et plomberie. Certificats reconnus. Cours du soir disponibles.",
                location="Rue Panaméricaine, Delmas 19",
                phone="3701-2233",
                hours="Lundi-Samedi: 8h-20h",
                user_id=users[3].id
            ),
        ]
        
        # Water & Sanitation
        water_services = [
            ServiceProvider(
                name="Point d'Eau Potable - Cité Soleil",
                category="Water & Sanitation",
                description="Station de distribution d'eau potable traitée. Prix abordable, service rapide. Bidons disponibles à l'achat.",
                location="Avenue N, Cité Soleil",
                phone="3722-8899",
                hours="Tous les jours: 6h-18h",
                user_id=users[1].id
            ),
            ServiceProvider(
                name="DINEPA - Bureau Régional",
                category="Water & Sanitation",
                description="Bureau régional pour signaler problèmes d'eau, demandes de connexion et urgences sanitaires.",
                location="Rue Legitimate, Tabarre",
                phone="2812-3344",
                hours="Lundi-Vendredi: 8h-16h",
                user_id=users[4].id
            ),
        ]
        
        # Community Centers
        community_services = [
            ServiceProvider(
                name="Centre Culturel et Communautaire de Pétion-Ville",
                category="Community Centers",
                description="Espace polyvalent pour événements communautaires, formations, rencontres. Salle climatisée avec équipement audiovisuel.",
                location="Rue Grégoire, Pétion-Ville",
                phone="2940-5566",
                hours="Lundi-Dimanche: 8h-22h (sur réservation)",
                user_id=users[3].id
            ),
            ServiceProvider(
                name="Église Baptiste de la Renaissance",
                category="Community Centers",
                description="Lieu de culte ouvert à tous. Programmes d'aide communautaire, distribution alimentaire mensuelle, et activités pour jeunes.",
                location="Boulevard Harry Truman, Carrefour",
                phone="3788-6677",
                hours="Dimanche: 9h-13h, Mercredi: 18h-20h, Activités quotidiennes",
                user_id=users[5].id
            ),
        ]
        
        # Emergency Services
        emergency_services = [
            ServiceProvider(
                name="Croix-Rouge Haïtienne - Antenne Ouest",
                category="Emergency Services",
                description="Services d'urgence, premiers secours, ambulance, et assistance en cas de catastrophe naturelle. Équipe disponible 24/7.",
                location="Boulevard Jean-Jacques Dessalines",
                phone="3701-1234",
                hours="24/7 - Urgences",
                user_id=users[0].id
            ),
            ServiceProvider(
                name="Police Nationale d'Haïti - Commissariat Centre-Ville",
                category="Emergency Services",
                description="Poste de police pour urgences, plaintes, et assistance sécuritaire. Personnel disponible en tout temps.",
                location="Champ de Mars, près du Palais National",
                phone="2223-3344",
                hours="24/7",
                user_id=users[4].id
            ),
        ]
        
        all_services = medical_services + education_services + water_services + community_services + emergency_services
        db.session.add_all(all_services)
        db.session.commit()
        print(f"✅ Created {len(all_services)} service providers")
        
        print("Creating reviews...")
        # Create Reviews
        reviews = [
            # Reviews for Hôpital Général
            Review(
                rating=4,
                comment="Service d'urgence efficace. J'ai été bien pris en charge malgré l'affluence. Personnel compétent.",
                user_id=users[2].id,
                service_provider_id=all_services[0].id
            ),
            Review(
                rating=3,
                comment="Bons médecins mais temps d'attente très long. Il faut améliorer l'organisation.",
                user_id=users[3].id,
                service_provider_id=all_services[0].id
            ),
            
            # Reviews for Clinique Delmas
            Review(
                rating=5,
                comment="Excellente clinique! Personnel accueillant et prix très abordables. Je recommande vivement.",
                user_id=users[4].id,
                service_provider_id=all_services[1].id
            ),
            Review(
                rating=5,
                comment="Ma famille se soigne ici depuis 3 ans. Service de qualité, jamais déçu.",
                user_id=users[0].id,
                service_provider_id=all_services[1].id
            ),
            
            # Reviews for Pharmacie
            Review(
                rating=4,
                comment="Prix corrects et bon conseil du pharmacien. Parfois en rupture de stock sur certains médicaments.",
                user_id=users[1].id,
                service_provider_id=all_services[2].id
            ),
            
            # Reviews for Bibliothèque
            Review(
                rating=5,
                comment="Endroit calme et propre pour étudier. Internet fonctionne bien. Excellent pour les étudiants!",
                user_id=users[3].id,
                service_provider_id=all_services[3].id
            ),
            Review(
                rating=4,
                comment="Bonne collection de livres. J'aimerais voir plus de livres récents mais c'est déjà très bien.",
                user_id=users[5].id,
                service_provider_id=all_services[3].id
            ),
            
            # Reviews for École Nationale
            Review(
                rating=4,
                comment="Mes enfants sont heureux dans cette école. Bons professeurs et environnement sécurisé.",
                user_id=users[0].id,
                service_provider_id=all_services[4].id
            ),
            
            # Reviews for Centre de Formation
            Review(
                rating=5,
                comment="J'ai fait ma formation en informatique ici. Excellents formateurs, j'ai trouvé du travail après!",
                user_id=users[1].id,
                service_provider_id=all_services[5].id
            ),
            Review(
                rating=5,
                comment="Formation pratique et utile. Les cours du soir sont parfaits pour ceux qui travaillent la journée.",
                user_id=users[2].id,
                service_provider_id=all_services[5].id
            ),
            
            # Reviews for Point d'Eau
            Review(
                rating=3,
                comment="Eau de bonne qualité mais parfois il y a beaucoup de queue. Il faudrait plus de robinets.",
                user_id=users[4].id,
                service_provider_id=all_services[6].id
            ),
            Review(
                rating=4,
                comment="Service correct et prix raisonnable. Personnel aimable.",
                user_id=users[5].id,
                service_provider_id=all_services[6].id
            ),
            
            # Reviews for Centre Culturel
            Review(
                rating=5,
                comment="Magnifique espace pour événements! Très bien équipé et personnel professionnel.",
                user_id=users[2].id,
                service_provider_id=all_services[8].id
            ),
            
            # Reviews for Croix-Rouge
            Review(
                rating=5,
                comment="Intervention rapide lors de l'urgence de mon père. Équipe professionnelle et dévouée. Merci!",
                user_id=users[1].id,
                service_provider_id=all_services[10].id
            ),
            Review(
                rating=5,
                comment="Service exemplaire. Toujours là quand la communauté en a besoin.",
                user_id=users[3].id,
                service_provider_id=all_services[10].id
            ),
        ]
        
        db.session.add_all(reviews)
        db.session.commit()
        print(f"✅ Created {len(reviews)} reviews")
        
        print("\n" + "="*50)
        print("🎉 SEED DATA CREATED SUCCESSFULLY!")
        print("="*50)
        print(f"Total Users: {User.query.count()}")
        print(f"Total Service Providers: {ServiceProvider.query.count()}")
        print(f"  - Medical/Health: {ServiceProvider.query.filter_by(category='Medical/Health').count()}")
        print(f"  - Education: {ServiceProvider.query.filter_by(category='Education').count()}")
        print(f"  - Water & Sanitation: {ServiceProvider.query.filter_by(category='Water & Sanitation').count()}")
        print(f"  - Community Centers: {ServiceProvider.query.filter_by(category='Community Centers').count()}")
        print(f"  - Emergency Services: {ServiceProvider.query.filter_by(category='Emergency Services').count()}")
        print(f"Total Reviews: {Review.query.count()}")
        print("="*50)

if __name__ == '__main__':
    seed_data()