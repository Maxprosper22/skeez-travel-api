// trip-card.js
class TripCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.tripData = {};
  }

  static get observedAttributes() {
    return ['trip-id', 'status', 'date', 'destination', 'slots', 'capacity', 'price'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      this.render();
    }
  }

  connectedCallback() {
    this.render();
  }

  setTripData(trip) {
    this.tripData = trip;
    this.render();
  }

  render() {
    const tripId = this.getAttribute('trip-id') || this.tripData.trip_id || 'N/A';
    const status = this.getAttribute('status') || this.tripData.status || 'Unknown';
    const date = this.getAttribute('date') || this.tripData.date || 'N/A';
    const destination = this.getAttribute('destination') || this.tripData.destination || 'N/A';
    const slots = this.getAttribute('slots') || this.tripData.slots || '0';
    const capacity = this.getAttribute('capacity') || this.tripData.capacity || '0';
    const price = this.getAttribute('price') || this.tripData.price || 'N/A';

    const template = document.getElementById('trip-card-template');
    if (!template) {
      console.error('Template with ID "trip-card-template" not found');
      return;
    }
    const templateContent = template.content.cloneNode(true);

    this.shadowRoot.innerHTML = '';
    this.shadowRoot.appendChild(templateContent);

    this.shadowRoot.querySelector('.trip-card').setAttribute('href', `trip/${tripId}`);
    this.shadowRoot.querySelector('.header-id span').textContent = tripId;
    this.shadowRoot.querySelector('.header-status span').textContent = status;
    this.shadowRoot.querySelector('.detail-item:nth-child(1) .detail-value').textContent = date;
    this.shadowRoot.querySelector('.detail-item:nth-child(2) .detail-value').textContent = destination;
    this.shadowRoot.querySelector('.detail-item:nth-child(3) .detail-value').textContent = `${slots}/${capacity}`;
    this.shadowRoot.querySelector('.detail-item:nth-child(4) .detail-value').textContent = price;
  }
}

customElements.define('trip-card', TripCard);
