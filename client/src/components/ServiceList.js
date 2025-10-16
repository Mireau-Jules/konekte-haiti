import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './ServiceList.css';

function ServiceList() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const categories = [
    'Medical/Health',
    'Education',
    'Water & Sanitation',
    'Community Centers',
    'Emergency Services'
  ];

  useEffect(() => {
    fetchServices();
  }, [selectedCategory]);

  const fetchServices = () => {
    setLoading(true);
    let url = '/api/service-providers';
    
    if (selectedCategory) {
      url += `?category=${selectedCategory}`;
    }

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch services');
        }
        return response.json();
      })
      .then(data => {
        setServices(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  };

  const filteredServices = services.filter(service =>
    service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="loading">Chargement des services...</div>;
  }

  if (error) {
    return <div className="error">Erreur: {error}</div>;
  }

  return (
    <div className="service-list">
      <h1>Services Communautaires en Haïti</h1>
      <p className="subtitle">Connectez-vous aux ressources essentielles de votre communauté</p>

      {/* Search and Filter */}
      <div className="filters">
        <input
          type="text"
          placeholder="Rechercher un service, lieu..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />

        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="category-select"
        >
          <option value="">Toutes les catégories</option>
          {categories.map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
      </div>

      {/* Service Cards */}
      <div className="services-grid">
        {filteredServices.length === 0 ? (
          <p className="no-results">Aucun service trouvé.</p>
        ) : (
          filteredServices.map(service => (
            <div key={service.id} className="service-card">
              <div className="service-category">{service.category}</div>
              <h3>{service.name}</h3>
              <p className="service-location">📍 {service.location}</p>
              <p className="service-description">
                {service.description.length > 150
                  ? `${service.description.substring(0, 150)}...`
                  : service.description}
              </p>
              <div className="service-info">
                {service.phone && (
                  <span className="service-phone">📞 {service.phone}</span>
                )}
                {service.hours && (
                  <span className="service-hours">🕐 {service.hours}</span>
                )}
              </div>
              {service.reviews && service.reviews.length > 0 && (
                <div className="service-rating">
                  ⭐ {(service.reviews.reduce((sum, r) => sum + r.rating, 0) / service.reviews.length).toFixed(1)} ({service.reviews.length} avis)
                </div>
              )}
              <Link to={`/services/${service.id}`} className="view-details-btn">
                Voir les détails
              </Link>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ServiceList;