class TripForm extends HTMLElement {
  static get observedAttribute() {
  }

  constructor() {
    super()
    this._active = this.hasAttribute('active')
    this.shadow = this.attachShadow({mode: "open"})
    const template = document.querySelector('#trip-form-template')
    this.shadow.appendChild(template.content.cloneNode(true))
 
    // console.log(this)
  }

  connectedCallback() {
    document.addEventListener("trip-form", event => {
      const container = this.shadow.querySelector('#trip-form-root')
      console.log(container)
      if (event.detail && event.detail.visible == true) {
        container.style.display = 'flex'
      } else {
        container.style.display = 'none'
      }
      console.log(event)
    })

    this.backdrop = this.shadow.querySelector('#form-back-drop')
  }

  disconnectedCallback() {
    this.backdrop.removeEventListener('trip-form')
  }
}

customElements.define("trip-form", TripForm)
