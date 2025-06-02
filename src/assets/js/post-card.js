class PostCard extends HTMLElement {
  static observedAttributes = ["avatar", "uid", "username", "firstname", "lastname", "date", "pid", "content", "media", "comments", "likes", "dislikes"]

  constructor() {
    super()
    const shadow = this.attachShadow({ mode: 'open' })
    const template = document.getElementById('#post-template').content.cloneNode(true)

    shadow.appendChild(template)
  }

  async connectedCallback() {

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
