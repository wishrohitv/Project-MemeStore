console.log("hello from index.js");

/// Initialize variable for
// Template of post preview macro
let postTemplate;
// Container of post preview
let postContainer;

function initializeTemplate() {
  fetch("/daisyUI/pureMacrosInHtml/postLayoutMacro.html")
    .then((res) => res.text())
    .then((templateHtml) => {
      // Insert the fetched template into a hidden container
      // console.log(templateHtml);
      const tempContainer = document.createElement("div");
      tempContainer.innerHTML = templateHtml;

      // Insert the fetched template into a dom alternative of above code
      //const doc = new DOMParser().parseFromString(templateHtml, 'text/html');
      //const template = doc.getElementById('postPreview');

      // Register macro in dome
      document.body.appendChild(tempContainer); // or keep it detached

      /// Assign html id of content to variable
      postTemplate = document.getElementById("postPreview");
      postContainer = document.getElementById("postContainer");
    });
}

// Function to fetch home feed for user
async function fetchHomeFeed() {
  initializeTemplate();
  let connection = await fetch(apiHomeFeed, {
    method: "GET",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
  });
  let res = await connection.json();
  try {
    if (connection.ok) {
      return res.payload;
    } else {
      return res.error;
    }
  } catch (error) {
    console.error(error);
    return error;
  }
}

async function loadHomeFeed() {
  /// Fetch home feed data
  feedData = await fetchHomeFeed();

  // Check if feedData is not empty
  if (feedData) {
    console.log(feedData);
    // Loop feedData list
    feedData.forEach((post) => {
      const clone = postTemplate.content.cloneNode(true);
      clone.querySelector(".cardTitle").textContent = post.title;
      clone.querySelector(".cardInfo").textContent = post.userID;
      clone.querySelector(".postUserName").textContent = post.userName;
      if (post.fileType === "image") {
        clone.querySelector(".postContentImgPreview").src = post.postMediaUrl;
      } else if (post.fileType === "video") {
        clone.querySelector(".postContentImgPreview").classList.add("hidden");
        clone
          .querySelector(".postContentVidPreview")
          .classList.remove("hidden");
        clone.querySelector(".postContentVidPreview").src = post.postMediaUrl;
      }
      clone.querySelector(".postUserPic").src = post.postUserPicUrl;

      // Link of creator's profile
      clone.querySelector(".postUserName").href = `/user/${post.userName}`;
      clone.querySelector(".userProfileLink").href = `/user/${post.userName}`;

      clone
        .querySelector(".btn")
        .addEventListener("click", () => togglePostLike(post.postID));
      postContainer.appendChild(clone);
    });
  } else {
    console.error(feedData);
  }
}

// Fetch home feed on page load
window.onload = function () {
  // initializeTemplate();
  loadHomeFeed();
};
