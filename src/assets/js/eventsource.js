// EventSourceService.js
class EventSourceService {
  constructor(url) {
    this.url = url;
    this.eventSource = null;
    this.tripCards = new Map();
  }

  registerTripCard(tripId, tripCard) {
    if (!this.tripCards.has(tripId)) {
      this.tripCards.set(tripId, new Set());
    }
    this.tripCards.get(tripId).add(tripCard);
  }

  unregisterTripCard(tripId, tripCard) {
    if (this.tripCards.has(tripId)) {
      this.tripCards.get(tripId).delete(tripCard);
      if (this.tripCards.get(tripId).size === 0) {
        this.tripCards.delete(tripId);
      }
    }
  }

  connect() {
    const tripIds = Array.from(this.tripCards.keys());
    const query = tripIds.length > 0 ? `?trip_id=${tripIds.join('&trip_id=')}` : '';
    this.eventSource = new EventSource(`${this.url}${query}`);

    this.eventSource.onopen = () => {
      console.log('EventSource connected');
    };

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (this.tripCards.has(data.trip_id)) {
          this.tripCards.get(data.trip_id).forEach((tripCard) => {
            tripCard.setTripData({
              trip_id: data.trip_id,
              status: data.status,
              date: data.date,
              destination: data.destination,
              slots: data.slots,
              capacity: data.capacity,
              price: data.price
            });
          });
        }
      } catch (error) {
        console.error('Error parsing SSE message:', error);
      }
    };

    this.eventSource.onerror = () => {
      console.error('EventSource error, reconnection handled automatically by EventSource');
    };
  }

  close() {
    if (this.eventSource) {
      this.eventSource.close();
      console.log('EventSource closed');
    }
  }
}
