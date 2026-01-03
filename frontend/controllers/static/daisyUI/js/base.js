// Api endpoint
const baseUrl = "http://127.0.0.1:5000";
// const baseUrl = "http://10.183.85.239:8000";
const apiLoginUser = `${baseUrl}/api/v1/auth/login`;
const apiSignupUser = `${baseUrl}/api/v1/auth/signup`;
const apiUploadPosts = `${baseUrl}/api/v1/posts/upload`;
const apiUserProfile = `${baseUrl}/api/v1/users`;
const apiProfileImage = `${baseUrl}/api/v1/getProfileImage/`;
const apiUpdateProfile = `${baseUrl}/api/v1/users/update`;
const apiUserPostsFeed = `${baseUrl}/api/v1/posts`;
const apiHomeFeed = `${baseUrl}/api/v1/feed`;
const apiAddFollower = `${baseUrl}/api/v1/users/addFollower`;
const apiTogglePostLike = `${baseUrl}/api/v1/posts/Like`;

let loggedUserUid = localStorage.getItem("uid");
let loggedUserName = localStorage.getItem("userName");
// Function to fetch user's profile image
async function fetchProfileImg(userName, imgBox) {
  try {
    let connection = await fetch(`${apiProfileImage}/${userName}`);
    let imgData = await connection.json();
    if (connection.ok) {
      console.log(imgData);
      imgBox.src = imgData["profileImg"];
    }
  } catch (error) {
    console.error("Profile error", error);
  }
}

// /// Initialize variable for
// // Template of post preview macro
// let postTemplate;
// // // Container of post preview
// // let postContainer;

// function initializeTemplate() {
//   fetch("/daisyUI/pureMacrosInHtml/postLayoutMacro.html")
//     .then((res) => res.text())
//     .then((templateHtml) => {
//       // Insert the fetched template into a hidden container
//       // console.log(templateHtml);
//       const tempContainer = document.createElement("div");
//       tempContainer.innerHTML = templateHtml;

//       // Insert the fetched template into a dom alternative of above code
//       //const doc = new DOMParser().parseFromString(templateHtml, 'text/html');
//       //const template = doc.getElementById('postPreview');

//       // Register macro in dome
//       document.body.appendChild(tempContainer); // or keep it detached

//       /// Assign html id of content to variable
//       postTemplate = document.getElementById("postPreview");
//       // postContainer = document.getElementById("userPostContainer");
//     });
// }

async function initializeTemplate() {
  const res = await fetch("/daisyUI/pureMacrosInHtml/postLayoutMacro.html");
  const templateHtml = await res.text();

  const tempContainer = document.createElement("div");
  tempContainer.innerHTML = templateHtml;

  document.body.appendChild(tempContainer);

  postTemplate = document.getElementById("postPreview");

  return postTemplate; // resolve when fully loaded
}
// Function to load session user profile logo
window.onload = async function () {
  // console.log("logo profile session user")
  // let profileLogo = document.getElementById("loggedProfileLogo")
  // if(loggedUserName!=null){
  //     fetchProfileImg(loggedUserName, profileLogo)
  // }
};
