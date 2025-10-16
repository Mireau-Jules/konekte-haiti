import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import AddReviewForm from './AddReviewForm';
import './ServiceDetail.css';

function ServiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/service-providers/${id}`)
      .then(res => res.json())
      .then(data => {
        setService(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Chargement...</div>;
  if (!service) return <div className="error">Service non trouvé</div>;

  const handleReviewAdded = () => {
    fetch(`/api/service-providers/${id}`)
      .then(res => res.json())
      .then(data => setService(data));
  };

  return (
    <div className="service-detail">
      <Link to="/" className="back-link">← Retour</Link>
      
      <div className="service-header">
        <h1>{service.name}</h1>
        <div className="service-category-badge">{service.category}</div>
      </div>

      <div className="service-content">
        <div className="service-info-section">
          <h2>Informations</h2>
          <p><strong>📍</strong> {service.location}</p>
          {service.phone && <p><strong>📞</strong> {service.phone}</p>}
          {service.hours && <p><strong>🕐</strong> {service.hours}</p>}
          <p>{service.description}</p>
        </div>

        <div className="reviews-section">
          <h2>Avis ({service.reviews ? service.reviews.length : 0})</h2>
          <AddReviewForm serviceId={service.id} onReviewAdded={handleReviewAdded} />
          
          {service.reviews && service.reviews.length > 0 ? (
            <div className="reviews-list">
              {service.reviews.map(review => (
                <div key={review.id} className="review-card">
                  <strong>{review.user.name}</strong>
                  <div className="review-rating">{'⭐'.repeat(review.rating)}</div>
                  <p>{review.comment}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-reviews">Pas d'avis encore</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ServiceDetail;
