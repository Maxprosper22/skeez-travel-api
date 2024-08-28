class PostCard extends HTMLElement {
  static observedAttributes = ["avatar", "username", "firstname", "lastname", "date", "content", "media", "comments", "likes", "dislikes"]

  constructor() {
    super()
    const shadow = this.attachShadow({ mode: 'open' })
  }

  async connectedCallback() {}
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
