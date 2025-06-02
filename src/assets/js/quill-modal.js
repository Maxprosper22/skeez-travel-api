class QuillModal extends HTMLElement {
  constructor() {
    super()

    // Attach a shadow DOM tree to this instance - the mode 'open' means you can access the shadow DOM from outside
    const shadow = this.attachShadow({ mode: 'open' });

    // Create the backdrop
    const backdrop = document.createElement('div')
    backdrop.className = 'backdrop';

    // Create the modala container
    const modal = document.createElement('div')
    modal.className = 'modal'

    // Create the editor container
    const editorContainer = document.createElement('div')
    editorContainer.id = 'editor-container'
    editorContainer.style.height = '300px'

    // Apply external style to the shadow DOM
    const style = document.createElement('style')
    style.textContent = `
      .backdrop: {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,.8);
        display: flex;
        justify-content: center,
        align-items: center;
        z-index: 1000;
      }
      .modal: {
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        width: 80%;
        max-width: 600px;
      }
    `
    shadow.appendChild(style)

    // Append the editor to the modal
    modal.appendChild(editorContainer);

    // Append the modal to the backdrop
    backdrop.appendChild(modal)

    // Append the backdrop to the shadow DOM
    shadow.appendChild(backdrop)


    // Initialize Quill after the element is added to the DOM 
    const script = document.createElement('script');
    script.src = '/static/libraries/quill/quill.js'
    script.onload = () => {
      const quill = new Quill(editorContainer, {
        theme: 'snow'
      })
    }
    shadow.appendChild(script)
  }

  connectedCallback() {
    // When the component is added to the document, it can be opened
    this.shadowRoot.querySelector('.backdrop').addEventListener('click', (e) => {
      if (e.target === this.shadowRoot.querySelector('.backdrop')) {
        this.close()
      }
    })
  }

  open() {
    this.style.display = 'block'
  }
  
  close() {
    this.style.display = 'none'
  }
}

customElements.define('quill-modal', QuillModal)
