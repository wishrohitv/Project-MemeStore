// Container of post preview
let postContainer = document.getElementById("postContainer");
// Function to fetch home feed for user
async function fetchHomeFeed() {
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
  initializeTemplate().then(async (postTemplate) => {
    /// Fetch home feed data
    feedData = await fetchHomeFeed();
    // Check if feedData is not empty
    if (feedData) {
      // postTemplate comming from base.js
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
  });
}

// Fetch home feed on page load
window.onload = function () {
  // initializeTemplate();
  loadHomeFeed();
};
