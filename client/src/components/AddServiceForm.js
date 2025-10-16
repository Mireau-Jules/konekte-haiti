import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import './AddServiceForm.css';

function AddServiceForm() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [submitError, setSubmitError] = useState(null);

  useEffect(() => {
    fetch('/api/users')
      .then(response => response.json())
      .then(data => setUsers(data))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  const categories = [
    'Medical/Health',
    'Education',
    'Water & Sanitation',
    'Community Centers',
    'Emergency Services'
  ];

  const validateForm = (values) => {
    const errors = {};

    if (!values.name) {
      errors.name = 'Le nom est requis';
    } else if (values.name.length < 3) {
      errors.name = 'Le nom doit contenir au moins 3 caractères';
    } else if (values.name.length > 150) {
      errors.name = 'Le nom doit contenir moins de 150 caractères';
    }

    if (!values.category) {
      errors.category = 'La catégorie est requise';
    }

    if (!values.description) {
      errors.description = 'La description est requise';
    } else if (values.description.length < 10) {
      errors.description = 'La description doit contenir au moins 10 caractères';
    } else if (values.description.length > 1000) {
      errors.description = 'La description doit contenir moins de 1000 caractères';
    }

    if (!values.location) {
      errors.location = 'La localisation est requise';
    } else if (values.location.length < 5) {
      errors.location = 'La localisation doit contenir au moins 5 caractères';
    }

    if (values.phone) {
      const cleanPhone = values.phone.replace(/[\s\-()]/g, '');
      if (!/^\d+$/.test(cleanPhone)) {
        errors.phone = 'Le numéro de téléphone ne doit contenir que des chiffres';
      } else if (cleanPhone.length < 8 || cleanPhone.length > 15) {
        errors.phone = 'Le numéro de téléphone doit contenir entre 8 et 15 chiffres';
      }
    }

    if (!values.user_id) {
      errors.user_id = 'Veuillez sélectionner un utilisateur';
    }

    return errors;
  };

  const handleSubmit = (values, { setSubmitting }) => {
    setSubmitError(null);

    fetch('/api/service-providers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...values,
        user_id: parseInt(values.user_id)
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => {
            throw new Error(err.error || 'Erreur lors de la création du service');
          });
        }
        return response.json();
      })
      .then(data => {
        alert('Service ajouté avec succès!');
        navigate(`/services/${data.id}`);
      })
      .catch(error => {
        setSubmitError(error.message);
        setSubmitting(false);
      });
  };

  return (
    <div className="add-service-form">
      <h1>Ajouter un Nouveau Service</h1>
      <p className="form-description">
        Aidez votre communauté en ajoutant un service essentiel
      </p>

      {submitError && (
        <div className="error-message">
          {submitError}
        </div>
      )}

      <Formik
        initialValues={{
          name: '',
          category: '',
          description: '',
          location: '',
          phone: '',
          hours: '',
          user_id: ''
        }}
        validate={validateForm}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form className="service-form">
            <div className="form-group">
              <label htmlFor="name">Nom du service *</label>
              <Field
                type="text"
                name="name"
                id="name"
                placeholder="Ex: Hôpital Général"
              />
              <ErrorMessage name="name" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="category">Catégorie *</label>
              <Field as="select" name="category" id="category">
                <option value="">Sélectionnez une catégorie</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </Field>
              <ErrorMessage name="category" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description *</label>
              <Field
                as="textarea"
                name="description"
                id="description"
                rows="4"
                placeholder="Décrivez les services offerts..."
              />
              <ErrorMessage name="description" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="location">Localisation *</label>
              <Field
                type="text"
                name="location"
                id="location"
                placeholder="Ex: Delmas 33, Port-au-Prince"
              />
              <ErrorMessage name="location" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="phone">Téléphone</label>
              <Field
                type="text"
                name="phone"
                id="phone"
                placeholder="Ex: 2222-3333"
              />
              <ErrorMessage name="phone" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="hours">Heures d'ouverture</label>
              <Field
                type="text"
                name="hours"
                id="hours"
                placeholder="Ex: Lundi-Vendredi: 8h-17h"
              />
              <ErrorMessage name="hours" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="user_id">Ajouté par *</label>
              <Field as="select" name="user_id" id="user_id">
                <option value="">Sélectionnez un utilisateur</option>
                {users.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.name}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="user_id" component="div" className="error" />
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="cancel-btn"
              >
                Annuler
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="submit-btn"
              >
                {isSubmitting ? 'Ajout en cours...' : 'Ajouter le service'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default AddServiceForm;