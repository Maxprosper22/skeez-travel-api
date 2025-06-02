class AdminTripView extends HTMLElement {
  static get observedAttributes() {
    return [
      "status",
      "slots",
      "eta"
    ]
  }

  constructor() {
    super();
  }

  connectedCallback() {
    this.shadow = this.attachShadow({
      mode: "open"
    })

    const template = document.getElementById("trip-template")
    shadow.appendChild(template.content.cloneNode(true))

    this.previewId = this.shadow.querySelector("#preview-id")
    this.previewStatus = this.shadow.querySelector('#preview-status')
    this.previewDestination = this.shadow.querySelector("#preview-destination")
    this.previewDate = this.shadow.querySelector("#preview-date")
    this.previewCapacity = this.shadow("#preview-capacity")
    this.viewStatus = this.shadow.querySelector("#view-status")
    this.viewDestinatination = this.shadow.querySelector("#view-destination")
    this.viewDestination = this.shadow.querySelector("#view-date")
    this.viewEta = this.shadow.querySelector("#view-eta")
    this.viewPassengers = this.shadow.querySelector("#view-passenger")
    this.viewCapacity = this.shadow.querySelector("#view-capacity")
    this.viewSlots = this.shadow.querySelector("#view-slots")
  }

  disconnectedCallback() {}

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue == newValue) {
      return
    }
    if (name == "status") {
      this.previewStatus.innerText = newValue
      this.viewStatus.innerText = newValue
    } else if (name == "slots") {
      this.viewSlots.innerText = newValue
    } else if (name == "date") {
      this.previewDate.innerText = newValue
    } if (name == "eta") {
      this.viewEta = newValue
    }
  }
}

customElements.define("admin-trip-view", AdminTripView);
