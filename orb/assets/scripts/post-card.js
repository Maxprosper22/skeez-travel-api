class PostCard extends HTMLElement {
  static observedAttributes = ["avatar", "uid", "username", "firstname", "lastname", "date", "pid", "content", "media", "comments", "likes", "dislikes"]

  constructor() {
    super()
    const shadow = this.attachShadow({ mode: 'open' })
  }

  async connectedCallback() {

    const template = document.getElementById('#template').content.cloneNode(true)

    shadow.append(template)
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
