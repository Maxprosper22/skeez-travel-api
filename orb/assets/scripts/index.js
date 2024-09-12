const index = async () => {

  const feedData = await fetch('/feed')

  if (feedData.code == 200) {
    feed = await feedData.json()
    if (feed.posts) {
      for (post=0; post < feed.posts.length; post++) {
        postCard = document.createElement('post-card')
        // postCard.setAttribute()
      }
    }
  } else {
    // document.getElementById('content').innerHTML = '<h1 class="dark:text-white">Home Page</h1><p class="dark:text-white">Welcome to the home page!</p>';
  }
}

document.getElementById('toggle-create-modal').addEventListener('click', () => {
  const createPostModal = document.querySelector('#create-post')
  createPostModal.toggleVisibility()
})
