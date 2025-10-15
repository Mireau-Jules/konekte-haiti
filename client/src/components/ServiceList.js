import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import AddReviewForm from './AddReviewForm';
import './ServiceDetail.css';

function ServiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showReviewForm, setShowReviewForm] = useState(false);

  useEffect(() => {
    fetchServiceDetail();
  }, [id]);

  const fetchServiceDetail = () => {
    fetch(`/api/service-providers/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Service non trouvé');
        }
        return response.json();
      })
      .then(data => {
        setService(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  };

  const handleDelete = () => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce service?')) {
      fetch(`/api/service-providers/${id}`, {
        method: 'DELETE',
      })
        .then(response => {
          if (response.ok) {
            alert('Service supprimé avec succès!');
            navigate('/');
          } else {
            throw new Error('Échec de la suppression');
          }
        })
        .catch(error => {
          alert('Erreur: ' + error.message);
        });
    }
  };

  const handleReviewAdded = () => {
    setShowReviewForm(false);
    fetchServiceDetail(); // Refresh to show new review
  };

  if (loading) {
    return <div className="loading">Chargement...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>Erreur: {error}</p>
        <Link to="/" className="back-link">← Retour à l'accueil</Link>
      </div>
    );
  }

  if (!service) {
    return <div className="error">Service non trouvé</div>;
  }

  return (
    <div className="service-detail">
      <Link to="/" className="back-link">← Retour aux services</Link>
      
      <div className="service-header">
        <div className="service-category-badge">{service.category}</div>
        <h1>{service.name}</h1>
        
        {service.average_rating > 0 && (
          <div className="rating-display">
            <span className="stars">⭐ {service.average_rating.toFixed(1)}</span>
            <span className="review-count">({service.reviews.length} avis)</span>
          </div>
        )}
      </div>

      <div className="service-content">
        <div className="service-info-section">
          <h2>Informations</h2>
          <div className="info-item">
            <strong>📍 Localisation:</strong>
            <p>{service.location}</p>
          </div>
          {service.phone && (
            <div className="info-item">
              <strong>📞 Téléphone:</strong>
              <p>{service.phone}</p>
            </div>
          )}
          {service.hours && (
            <div className="info-item">
              <strong>🕐 Heures d'ouverture:</strong>
              <p>{service.hours}</p>
            </div>
          )}
          <div className="info-item">
            <strong>📝 Description:</strong>
            <p>{service.description}</p>
          </div>
        </div>

        <div className="service-actions">
          <button onClick={handleDelete} className="delete-btn">
            Supprimer ce service
          </button>
        </div>

        <div className="reviews-section">
          <div className="reviews-header">
            <h2>Avis de la communauté ({service.reviews.length})</h2>
            <button 
              onClick={() => setShowReviewForm(!showReviewForm)}
              className="add-review-btn"
            >
              {showReviewForm ? 'Annuler' : '+ Ajouter un avis'}
            </button>
          </div>

          {showReviewForm && (
            <AddReviewForm 
              serviceId={service.id} 
              onReviewAdded={handleReviewAdded}
            />
          )}

          <div className="reviews-list">
            {service.reviews.length === 0 ? (
              <p className="no-reviews">Aucun avis pour le moment. Soyez le premier à donner votre avis!</p>
            ) : (
              service.reviews.map(review => (
                <div key={review.id} className="review-card">
                  <div className="review-header">
                    <div className="review-author">
                      <strong>{review.user.name}</strong>
                      <span className="review-date">
                        {new Date(review.created_at).toLocaleDateString('fr-FR')}
                      </span>
                    </div>
                    <div className="review-rating">
                      {'⭐'.repeat(review.rating)}
                    </div>
                  </div>
                  <p className="review-comment">{review.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ServiceDetail;