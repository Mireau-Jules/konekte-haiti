import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AddReviewForm from './AddReviewForm';
import './ServiceDetail.css';

function ServiceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/services/${id}`)
      .then(res => res.json())
      .then(data => {
        setService(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!service) return <div>Service not found</div>;

  return (
    <div className="service-detail">
      <button onClick={() => navigate(-1)}>← Back</button>
      <h1>{service.name}</h1>
      <p>{service.description}</p>
      <div className="service-info">
        <p><strong>Category:</strong> {service.category}</p>
        <p><strong>Location:</strong> {service.location}</p>
        <p><strong>Contact:</strong> {service.contact}</p>
      </div>
      
      <h2>Reviews</h2>
      {service.reviews && service.reviews.map(review => (
        <div key={review.id} className="review">
          <p><strong>Rating:</strong> {review.rating}/5</p>
          <p>{review.comment}</p>
        </div>
      ))}
      
      <AddReviewForm serviceId={id} />
    </div>
  );
}

export default ServiceDetail;