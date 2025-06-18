/* Custom JavaScript for Real Estate Price Predictor */

class RealEstatePredictor {
    constructor() {
        this.map = null;
        this.selectedMarker = null;
        this.defaultLocation = [23.0225, 72.5714]; // Ahmedabad center
        this.init();
    }

    init() {
        this.initMap();
        this.bindEvents();
        this.setDefaultLocation();
    }

    initMap() {
        // Initialize map
        this.map = L.map('map').setView(this.defaultLocation, 12);
        
        // Add tile layer with better styling
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18,
        }).addTo(this.map);

        // Add city boundaries (optional enhancement)
        this.addCityBoundaries();
        
        // Bind map events
        this.map.on('click', (e) => this.onMapClick(e));
    }

    addCityBoundaries() {
        // Add a circle to show Ahmedabad city area
        const cityCircle = L.circle(this.defaultLocation, {
            color: '#3498db',
            fillColor: '#3498db',
            fillOpacity: 0.1,
            radius: 15000 // 15km radius
        }).addTo(this.map);

        cityCircle.bindPopup('Ahmedabad City Area<br>Best prediction accuracy within this region');
    }

    onMapClick(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Remove previous marker
        if (this.selectedMarker) {
            this.map.removeLayer(this.selectedMarker);
        }
        
        // Add new marker with custom styling
        this.selectedMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'custom-marker',
                html: '<i class="fas fa-map-marker-alt text-danger" style="font-size: 2rem;"></i>',
                iconSize: [30, 30],
                iconAnchor: [15, 30]
            })
        }).addTo(this.map);

        // Create popup content
        const popupContent = `
            <div class="text-center">
                <strong>Selected Property Location</strong><br>
                <small>Lat: ${lat.toFixed(6)}, Lng: ${lng.toFixed(6)}</small><br>
                <button class="btn btn-sm btn-primary mt-2" onclick="predictor.centerOnLocation(${lat}, ${lng})">
                    <i class="fas fa-crosshairs me-1"></i>Center Here
                </button>
            </div>
        `;
        
        this.selectedMarker.bindPopup(popupContent).openPopup();
        
        // Update form fields
        this.updateLocationFields(lat, lng);
        
        // Add subtle animation
        this.selectedMarker.getElement()?.classList.add('fade-in-up');
    }

    updateLocationFields(lat, lng) {
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lng;
        document.getElementById('selected-lat').value = lat.toFixed(6);
        document.getElementById('selected-lng').value = lng.toFixed(6);
    }

    setDefaultLocation() {
        const [lat, lng] = this.defaultLocation;
        
        // Add default marker
        const defaultMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'custom-marker-default',
                html: '<i class="fas fa-city text-primary" style="font-size: 1.5rem;"></i>',
                iconSize: [25, 25],
                iconAnchor: [12, 25]
            })
        }).addTo(this.map);

        defaultMarker.bindPopup(`
            <div class="text-center">
                <strong>Ahmedabad City Center</strong><br>
                <small>Click anywhere on the map to select a property location</small>
            </div>
        `).openPopup();

        this.updateLocationFields(lat, lng);
    }

    centerOnLocation(lat, lng) {
        this.map.setView([lat, lng], 15);
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('prediction-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handlePrediction(e));
        }

        // Real-time form validation
        this.addFormValidation();
    }

    addFormValidation() {
        const inputs = document.querySelectorAll('#prediction-form input, #prediction-form select');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateField(input));
            input.addEventListener('change', () => this.validateField(input));
        });
    }

    validateField(field) {
        const value = field.value;
        let isValid = true;
        let message = '';

        switch (field.name) {
            case 'square_feet':
                const area = parseFloat(value);
                isValid = area >= 200 && area <= 10000;
                message = isValid ? '' : 'Area must be between 200 and 10,000 sq ft';
                break;
            case 'bedrooms':
            case 'bathrooms':
                isValid = value !== '';
                message = isValid ? '' : 'Please select a value';
                break;
        }

        this.updateFieldValidation(field, isValid, message);
    }

    updateFieldValidation(field, isValid, message) {
        const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                        this.createFeedbackElement(field.parentNode);
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            feedback.textContent = '';
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            feedback.textContent = message;
        }
    }

    createFeedbackElement(parent) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        parent.appendChild(feedback);
        return feedback;
    }

    async handlePrediction(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }

        this.showLoading(true);
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayPrediction(result.prediction, data);
                this.logPrediction(result);
            } else {
                this.showError('Prediction failed: ' + result.error);
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    validateForm() {
        const form = document.getElementById('prediction-form');
        const inputs = form.querySelectorAll('input[required], select[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value) {
                this.updateFieldValidation(input, false, 'This field is required');
                isValid = false;
            }
        });

        return isValid;
    }

    displayPrediction(prediction, inputData) {
        // Update price display
        document.getElementById('predicted-price').textContent = 
            this.formatCurrency(prediction.predicted_price);
        document.getElementById('price-lower').textContent = 
            this.formatCurrency(prediction.lower_bound);
        document.getElementById('price-upper').textContent = 
            this.formatCurrency(prediction.upper_bound);
        document.getElementById('prediction-date').textContent = 
            new Date(prediction.prediction_date).toLocaleString();

        // Show results with animation
        const resultsDiv = document.getElementById('prediction-results');
        resultsDiv.style.display = 'block';
        resultsDiv.classList.add('fade-in-up');

        // Add property summary
        this.addPropertySummary(inputData);
        
        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    addPropertySummary(data) {
        const summaryHTML = `
            <div class="mt-3 p-3 bg-light rounded">
                <h6><i class="fas fa-home me-2"></i>Property Summary</h6>
                <div class="row">
                    <div class="col-6">
                        <small><strong>Bedrooms:</strong> ${data.bedrooms}</small><br>
                        <small><strong>Bathrooms:</strong> ${data.bathrooms}</small>
                    </div>
                    <div class="col-6">
                        <small><strong>Area:</strong> ${data.square_feet} sq ft</small><br>
                        <small><strong>Age:</strong> ${data.property_age} years</small>
                    </div>
                </div>
            </div>
        `;
        
        const resultsDiv = document.getElementById('prediction-results');
        const existingSummary = resultsDiv.querySelector('.property-summary');
        if (existingSummary) {
            existingSummary.remove();
        }
        
        const summaryDiv = document.createElement('div');
        summaryDiv.className = 'property-summary';
        summaryDiv.innerHTML = summaryHTML;
        resultsDiv.querySelector('.prediction-result').appendChild(summaryDiv);
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const results = document.getElementById('prediction-results');
        
        if (show) {
            loading.style.display = 'block';
            results.style.display = 'none';
        } else {
            loading.style.display = 'none';
        }
    }

    showError(message) {
        // Create toast notification
        const toast = this.createToast('Error', message, 'danger');
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    createToast(title, message, type = 'info') {
        const toastHTML = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${title}:</strong> ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        const toastContainer = document.querySelector('.toast-container') || 
                             this.createToastContainer();
        
        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHTML;
        const toast = toastElement.firstElementChild;
        
        toastContainer.appendChild(toast);
        
        // Initialize Bootstrap toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        return toast;
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '11';
        document.body.appendChild(container);
        return container;
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    logPrediction(result) {
        // Log prediction for analytics (optional)
        console.log('Prediction made:', {
            timestamp: new Date().toISOString(),
            prediction: result.prediction,
            input: result.input_data
        });
    }
}

// Initialize the predictor when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.predictor = new RealEstatePredictor();
});

// Utility functions
function downloadPrediction() {
    const prediction = document.getElementById('predicted-price').textContent;
    const date = new Date().toLocaleDateString();
    
    const data = `Real Estate Price Prediction\nDate: ${date}\nPredicted Price: ${prediction}\n`;
    
    const blob = new Blob([data], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `property_prediction_${date.replace(/\//g, '-')}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function sharePrediction() {
    const prediction = document.getElementById('predicted-price').textContent;
    const text = `Check out this property price prediction: ${prediction}`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Property Price Prediction',
            text: text,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
            alert('Prediction copied to clipboard!');
        });
    }
}
