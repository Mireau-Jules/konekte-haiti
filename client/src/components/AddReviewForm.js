import React, { useState, useEffect } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import './AddReviewForm.css';

function AddReviewForm({ serviceId, onReviewAdded }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch users for the dropdown
    fetch('/api/users')
      .then(response => response.json())
      .then(data => setUsers(data))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  const validateForm = (values) => {
    const errors = {};

    // Rating validation (data type - must be integer between 1-5)
    if (!values.rating) {
      errors.rating = 'La note est requise';
    } else if (isNaN(parseInt(values.rating))) {
      errors.rating = 'La note doit être un nombre';
    } else {
      const rating = parseInt(values.rating);
      if (rating < 1 || rating > 5) {
        errors.rating = 'La note doit être entre 1 et 5';
      }
    }

    // Comment validation (string length)
    if (!values.comment) {
      errors.comment = 'Le commentaire est requis';
    } else if (values.comment.length < 5) {
      errors.comment = 'Le commentaire doit contenir au moins 5 caractères';
    } else if (values.comment.length > 500) {
      errors.comment = 'Le commentaire doit contenir moins de 500 caractères';
    }

    // User validation (data type)
    if (!values.user_id) {
      errors.user_id = 'Veuillez sélectionner un utilisateur';
    }

    return errors;
  };

  const handleSubmit = (values, { setSubmitting, resetForm, setErrors }) => {
    fetch('/api/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        rating: parseInt(values.rating),
        comment: values.comment,
        user_id: parseInt(values.user_id),
        service_provider_id: parseInt(serviceId)
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => {
            throw new Error(err.error || 'Erreur lors de l\'ajout de l\'avis');
          });
        }
        return response.json();
      })
      .then(() => {
        alert('Avis ajouté avec succès!');
        resetForm();
        onReviewAdded();
      })
      .catch(error => {
        setErrors({ submit: error.message });
        setSubmitting(false);
      });
  };

  return (
    <div className="add-review-form">
      <h3>Laisser un avis</h3>
      
      <Formik
        initialValues={{
          rating: '',
          comment: '',
          user_id: ''
        }}
        validate={validateForm}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, errors }) => (
          <Form className="review-form">
            {errors.submit && (
              <div className="error-message">{errors.submit}</div>
            )}

            <div className="form-group">
              <label htmlFor="user_id">Votre nom *</label>
              <Field as="select" name="user_id" id="user_id">
                <option value="">Sélectionnez votre nom</option>
                {users.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.name}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="user_id" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="rating">Note *</label>
              <Field as="select" name="rating" id="rating">
                <option value="">Choisir une note</option>
                <option value="5">⭐⭐⭐⭐⭐ Excellent</option>
                <option value="4">⭐⭐⭐⭐ Très bien</option>
                <option value="3">⭐⭐⭐ Bien</option>
                <option value="2">⭐⭐ Acceptable</option>
                <option value="1">⭐ Mauvais</option>
              </Field>
              <ErrorMessage name="rating" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="comment">Votre commentaire *</label>
              <Field
                as="textarea"
                name="comment"
                id="comment"
                rows="4"
                placeholder="Partagez votre expérience..."
              />
              <ErrorMessage name="comment" component="div" className="error" />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="submit-review-btn"
            >
              {isSubmitting ? 'Envoi en cours...' : 'Publier l\'avis'}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default AddReviewForm;