document.addEventListener("DOMContentLoaded", () => {
  const postForm = document.getElementById("postForm");
  const feed = document.getElementById("feed");

  // Nav and post form show/hide logic
  const showPostFormLink = document.getElementById("showPostFormLink");
  const cancelPostNavLink = document.getElementById("cancelPostNavLink");
  const cancelPostBtn = document.getElementById("cancelPostBtn");

  function openPostForm() {
    postForm.style.display = "block";
    showPostFormLink.style.display = "none";
    cancelPostNavLink.style.display = "inline-block";
    document.getElementById("topic").focus();
  }
  function closePostForm() {
    postForm.style.display = "none";
    showPostFormLink.style.display = "inline-block";
    cancelPostNavLink.style.display = "none";
  }
  showPostFormLink.onclick = function(e) {
    e.preventDefault();
    openPostForm();
  };
  cancelPostBtn.onclick = function() {
    closePostForm();
  };
  cancelPostNavLink.onclick = function(e) {
    e.preventDefault();
    closePostForm();
  };

  // Fetch all posts
  fetch("/api/feed/", {
    credentials: "include"  // 👈 Send session cookie
  })
    .then(res => res.json())
    .then(data => {
      data.forEach(post => {
        feed.appendChild(makePostElement(post));
      });
    });

  // Handle new post submission
  postForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const content = document.getElementById("content").value;
    const topic = document.getElementById("topic").value;
    const timeSpent = document.getElementById("timeSpent").value;

    // Validate timeSpent: must be a decimal number with up to one decimal place
    if (!/^\d+(\.\d)?$/.test(timeSpent)) {
      alert("Please enter a valid time spent (number, up to one decimal place, e.g. 2 or 2.5)");
      return;
    }

    fetch("/api/post/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      credentials: "include",  // 👈 Send session cookie for auth
      body: JSON.stringify({ content, topic, time_spent: timeSpent })
    })
    .then(res => res.json())
    .then(post => {
      feed.prepend(makePostElement(post));
      postForm.reset();
      postForm.style.display = "none";
      document.getElementById("showPostFormBtn").style.display = "block";
    });
  });

  // Utility: build post element
  function makePostElement(post) {
    const div = document.createElement("div");
    div.className = "post";
    div.innerHTML = `
      <p><strong>@${post.username}</strong></p>
      <p>${post.content}</p>
      <small>${post.topic} • ${post.time_spent} • ${new Date(post.created_at).toLocaleString()}</small>
    `;
    return div;
  }

  // Utility: CSRF token
  function getCSRFToken() {
    const name = "csrftoken";
    const cookieValue = document.cookie.split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
    return cookieValue;
  }
});
