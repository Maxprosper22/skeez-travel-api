class PostCard extends HTMLElement {
  constructor() {
    super()
  }

  connectedCallback() {
    const shadow = this.attachShadow({ mode: 'open' })
  }
  disconnectedCallback() {}
  adoptedCallback() {}
  attributeChangedCallback(property, oldValue, newValue) {
    if (oldValue === newValue) {
      return;
    }
    this[property] = newValue
  }

}

customElements.define('post-card', PostCard)
