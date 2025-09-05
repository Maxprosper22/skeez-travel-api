const fetch_trips = async (e) => {
  const response = await fetch('/api/trips')
  res = await response.json()

  if (res.data && res.data.length > 0) {
    tripData = res.data
    tripData.forEach(trip => {
      try {
        sseService.registerTripCard(trip.trip_id, trip)
      } catch(e) {
        console.error(e);
        
        throw new Error('Unable to connect' + e)
      }

      const tripCard = document.createElement('trip-card');
      tripCard.setAttribute('trip-id', trip.trip_id);
      tripCard.setAttribute('status', trip.status);
      tripCard.setAttribute('date', new Date(trip.date).toDateString());
      tripCard.setAttribute('destination', trip.destination);
      tripCard.setAttribute('slots', trip.slots.length);
      tripCard.setAttribute('capacity', trip.capacity);
      document.querySelector('#card-container').appendChild(tripCard);
    });
  } else {
      document.querySelector('#card-container').innerHTML = 'No trips available';
  }
}

window.addEventListener('DOMContentLoaded', fetch_trips)
