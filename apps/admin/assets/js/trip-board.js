const openTripForm = new CustomEvent(
  "trip-form",
  {
    bubbles: true,
    composed: true,
    detail: {
      visible: true
    }
  }
)

const closeTripForm = new CustomEvent(
  "trip-form",
  {
    bubbles: true,
    composed: true,
    detail: {
      visible: false
    }
  }
)

// Trip form container
const tripForm = document.querySelector('#form-root')
tripForm.addEventListener("trip-form", function(event) {
  console.log(this)
  if (event.detail.visible && this.style.display == 'none') {
    this.style.display = 'flex'
  } else {
    this.style.display == 'none'
  }
})

//Trip form container back drop element
const backDrop = document.querySelector('#modal-backdrop')
backDrop.addEventListener('click', event => {
  event.target.parentElement.style.display = 'none'

})

// Button to pop up new trip form
const createTripBtn = document.querySelector('#new-trip-btn')
createTripBtn.addEventListener('click', event => {
  tripForm.style.display = 'flex'
})

const fetchTrips = async () => {
  const response = await fetch('admin/trips/')
  if (!response.ok) throw new Error("Network response was not ok")

  const tripData = await response.json();
  
  const tripContainer = document.getElementById("#trip-container5")

  tripData.forEach(trip => {
    const tripCard = docunent.createElement("admin-trip-view")
    tripCard.setAttribute('id', trip.trip_id)
    tripCard.setAttribute('destination', trip.destination)
    tripCard.setAttribute('date', trip.date)
    tripCard.setAttribute('slots', trip.slots)
    tripCard.setAttribute('status', trip.status)
    tripCard.setAttribute('capacity', trip.capacity)
  });
}

window.addEventListener('DOMContentLoaded', async () => {})

const submitNewTrip = async (event) => {
  // Submits trip daya to server
  const dateField = document.querySelector("#date-field")
  const destinationField = document.querySelector("#destination-field")
  const capacityField = document.querySelector("#capacity-field")
  const statusField = document.querySelector("#status-field")

  // console.log(statusField.value)

  if (dateField.value == "" || destinationField.value == "" || capacityField.value== "" || statusField.value == "") {
    Toastify({
      text: "Some fields are missing",
      // duration: 3000,
      destination: "https://github.com/apvarun/toastify-js",
      newWindow: true,
      close: true,
      gravity: "top", // `top` or `bottom`
      position: "center", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
        background: "linear-gradient(to right, #00b09b, #96c93d)",
      },
      onClick: function(){} // Callback after click
    }).showToast();

  } else {
    const response = await fetch('/admin/trip/create', {
      method: 'POST',
      body: JSON.stringify({
        'date': dateField.value,
        'destination': destinationField.value,
        'capacity': capacityField.value,
        'status': statusField.value
      })
    })

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
  }

}

const validateDestination = async () => {

}
const validateCapacity = async () => {}
const validateDate = async () => {}
const validateStatus = async () => {}
