let profileImg = document.getElementById("profileImg");
let followerCount = document.getElementById("followerCount");
let followingCount = document.getElementById("followingCount");
let name = document.getElementById("uName");
let userName_ = document.getElementById("userName");
let bio = document.getElementById("bio");
let uid = document.getElementById("uid");
// Container of post preview
let postContainer = document.getElementById("userPostContainer");
// function to fetch user's profile data
async function fetchUserProfileData(userName) {
  console.log("fetchUserProfileData");
  try {
    let connection = await fetch(`${apiUserProfile}/${userName}`, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    });
    let res = await connection.json();
    if (connection.ok) {
      name.appendChild(document.createTextNode(res.payload["name"]));
      userName_.appendChild(document.createTextNode(res.payload["userName"]));
      followerCount.innerText = `${res.payload["followerCount"]} follower`;
      followingCount.innerText = `${res.payload["followingCount"]} following`;

      // Load posts
      loadHomeFeed(userName);
    }
    console.error(res);
  } catch (e) {
    console.error(e);
  }
}

// Function to fetch home feed for user
async function fetchHomeFeed(userName) {
  let connection = await fetch(`${apiUserPostsFeed}/${userName}`, {
    method: "GET",
    credentials: "include",
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

async function loadHomeFeed(userName) {
  /// Fetch home feed data
  feedData = await fetchHomeFeed(userName);

  // Check if feedData is not empty
  if (feedData) {
    // Call postTemplate to load
    await initializeTemplate();
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

      // Link of creators profile
      clone.querySelector(".postUserName").href = `/user/${post.userName}`;
      clone.querySelector(".userProfileLink").href = `/user/${post.userName}`;
      postContainer.appendChild(clone);
    });
  } else {
    console.error(feedData);
  }
}

window.onload = function () {};

// Functon to addFollower
async function addFollower() {
  let userID = document.getElementById("uid");
  let connection = await fetch(apiAddFollower, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({ userID: userID.value }),
  });
  let res = await connection.json();

  console.log(res);
}

function router() {
  const path = location.pathname;
  const paths = path.split("/");
  // ['', 'user', 'pmModi']
  if (paths[1] === "user") {
    fetchUserProfileData(paths[2]);
    console.log("profile path", profileImg);
    fetchProfileImg(paths[2], profileImg);
  }
}

function navigate(url) {
  history.pushState({}, "", url);
  router();
}

window.addEventListener("popstate", router);
router();
