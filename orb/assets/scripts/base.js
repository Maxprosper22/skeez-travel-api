

function createPost() {
  document.getElementById('content').innerHTML = '<h1>About Page</h1><p>Learn more about us here.</p>';
}

function notification() {
  document.getElementById('content').innerHTML = '<h1>Contact Page</h1><p>Contact us here.</p>';
}

page('/', home);
page('/about', about);
page('/contact', contact);

// Start the router
page();
