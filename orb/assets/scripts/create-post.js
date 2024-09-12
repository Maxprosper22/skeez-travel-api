class CreatePost extends HTMLElement {
  static observedAttributes = ['open']

  constructor () {
    super()
    const shadow = this.attachShadow({ mode: 'open' })

    const template = document.getElementById('create-post-template').content.cloneNode(true)
    shadow.appendChild(template)

    // Inject Tailwind CSS into the shadow DOM
    const style = document.createElement('style');
    style.textContent = `
    @import url("/static/css/output.css");`;

    // Inject Quill JS into shadow DOM
    // const quill_script = document.createElement('script')
    // quill_script.src = 'https://cdn.quilljs.com/1.3.7/quill.js'
    // quill_script.onload = () => {
    //   const editorContainer = shadow.getElementById('editor-container');
    //   const quill = new Quill(editorContainer)
    //   shadow.appendChild(style);
    // }
    // shadow.appendChild(quill_script)

    // Inject CKEditor 5 Script
    const ckeditorScript = document.createElement('script');
    ckeditorScript.src = ''; // Replace with your CKEditor 5 URL
    ckeditorScript.onload = () => {
      // Initialize CKEditor 5
      ClassicEditor
        .create(shadow.getElementById('editor-container'), {
          // ... CKEditor 5 Configuration Options
        })
        .then(editor => {
          console.log('CKEditor 5 instance ready:', editor);
        })
        .catch(error => {
          console.error('CKEditor 5 failed to load:', error);
        });
    };
    shadow.appendChild(ckeditorScript);
  }

  connectedCallback() {}

  disconnectedCallback() {}

  adoptedCallback() {}

  attributeChangedCallback(property, oldValue, newValue) {
    if (property === 'open') {
      if (newValue === 'true') {
        this.toggleVisibility();
      } else {
        this.toggleVisibility();
      }
    }
  }

  toggleVisibility() {
    const container = this.shadowRoot.getElementById('container');
    if (container.style.display != 'none') {
      container.style.display = 'none';
    } else {
      container.style.display = 'flex';
    }
  }
}

// customElements.define('create-post', CreatePost)

tinymce.init({
  selector: '#editor-container',
  plugins: 'lists link image table code',
  toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | code',
  menubar: false,
  height: 300,
});
