class TripForm extends HTMLElement {
  static get observedAttribute() {
    return ['visible']
  }

  constructor() {
    super()
    // console.log(this)
  }

  connectedCallback() {
    this.shadow = this.attachShadow({mode: "open"})
    const template = document.querySelector('#trip-form-template')
    this.shadow.appendChild(template.content.cloneNode(true))
 
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
    const formModal = this.shadow.querySelector('#form-modal')
    formModal.addEventListener("trip-form", function(event) {
      console.log(this)
      console.log(event)

      if (event.detail.visible && event.target.style.display == 'none') {
        this.style.display = 'flex'
      } else {
        this.style.display == 'none'
      }
    })

    // Button to pop up new trip form
    const createTripBtn = this.shadow.querySelector('#new-trip-btn')
    createTripBtn.addEventListener('click', event => {
      // tripForm.style.display = 'flex'
        createTripBtn.dispatchEvent(openTripForm)
    })

    const backdrop = this.shadow.querySelector('#form-back-drop')

    backdrop.addEventListener("click", event => {
      backdrop.dispatchEvent(closeTripForm)
    })
  }

  disconnectedCallback() {
    this.backdrop.removeEventListener('trip-form')
  }
}

customElements.define("trip-form", TripForm)
