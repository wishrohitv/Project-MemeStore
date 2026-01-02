let name = document.getElementById("uName");
let userName = document.getElementById("userName");
let bio = document.getElementById("bio");
let uid = document.getElementById("uid");

// function to fetch user's profile data
console.log(loggedUserName, "alpha");
async function fetchUserProfileData() {
  console.log("sssssssssssssssssssssssssssssssss");
  try {
    let connection = await fetch(`${apiUserProfile}/${userName.innerText}`, {
      method: "GET",
      // credentials: "include",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    });
    let res = await connection.json();
    if (connection.ok) {
      name.appendChild(document.createTextNode(res.payload["name"]));
      userName.appendChild(document.createTextNode(res.payload["userName"]));
    }
    console.error(res);
  } catch (e) {
    console.error(e);
  }
}
// fetchUserProfileData();
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
      postContainer = document.getElementById("userPostContainer");
    });
}

// Function to fetch home feed for user
async function fetchHomeFeed() {
  let connection = await fetch(apiUserPostsFeed + uid.value, {
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

      // Link of creators profile
      clone.querySelector(".postUserName").href = `/user/${post.userName}`;
      clone.querySelector(".userProfileLink").href = `/user/${post.userName}`;
      postContainer.appendChild(clone);
    });
  } else {
    console.error(feedData);
  }
}

window.onload = function () {
  let profileLogo = document.getElementById("loggedProfileImg");
  if (userName.innerText != null) {
    fetchProfileImg(userName.innerText, profileLogo);

    initializeTemplate();
    loadHomeFeed();
  }
};

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
