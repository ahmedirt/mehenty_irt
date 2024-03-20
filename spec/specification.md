#membre de l'equipe: 23044, 23104, 23243
#le chef de l'equipe: 23243 
#git@github.com:ahmedirt/mehenty_irt.git
#Compte Rendu
1-a) Description du premier besoin fonctionnel: gestion de demande de service
Fonctionnalité: soumission de demande de service
Description Permettre aux clients de soumettre des demandes de service via
l’application mobile
Entrées Données de la demande de service
Source Interaction directe avec l’application mobile
Sorties Notification de réception de la demande pour le client
Destination Base de données des services de demandes
Actions Remplir le formulaire de demande
Pré-condition L’utilisateur doit être connecté à son compte sur l’application
mobile.
Post-condition La demande est enregistrée dans le système et transmise aux
techniciens disponibles pour traitement.
Effet de bord Enregistrement de la demande dans le système
b) Deuxième besoin fonctionnel: Attribution des services aux techniciens
Fonctionnalité: Attribution des services aux techniciens
Description Assigner automatiquement les demandes
de service aux techniciens disponibles en
fonction de leur disponibilité et de leur
emplacement
Entrées Nouvelle demande de service, liste des
techniciens disponibles
Source Automatique suite à la soumission d’une
demande par le client
Sorties Notification de la demande de service pour
le technicien attribué
Destination Affectation de la demande de service au
technicien attribué
Actions Identifier les techniciens adéquats, attribuer
la demande de service
Pré-condition Des demandes de service ont été soumises
par les clients et des techniciens sont
disponibles dans le système
Post-condition La demande de service est attribuée à un
technicien et les informations pertinentes
sont mises à sa disposition pour effectuer
l’intervention
Effet de bord Mise à jour de l’état de la demande dans le
système
