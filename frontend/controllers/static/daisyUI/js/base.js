console.log("from base");

// Api endpoint
const baseUrl = "http://127.0.0.1:5000";
// const baseUrl = "http://10.183.85.239:8000";
const apiAuthenticateUser = `${baseUrl}/api/v1/auth/login`;
const apiUploadPosts = `${baseUrl}/api/v1/uploadPosts`;
const apiUserProfile = `${baseUrl}/api/v1/users`;
const apiProfileImage = `${baseUrl}/api/v1/getProfileImage/`;
const apiUpdateProfile = `${baseUrl}/api/v1/updateProfile`;
const apiUserPostsFeed = `${baseUrl}/api/v1/userPostsFeed/`;
const apiHomeFeed = `${baseUrl}/api/v1/feed`;
const apiAddFollower = `${baseUrl}/api/v1/addFollower`;
const apiTogglePostLike = `${baseUrl}/api/v1//postLike`;

let loggedUserUid = localStorage.getItem("uid");
let loggedUserName = localStorage.getItem("userName");
console.log(loggedUserUid);
console.log(loggedUserName);

// Function to fetch user's profile image
async function fetchProfileImg(userName, imgBox) {
  let connection = await fetch(apiProfileImage + userName);
  let imgData = await connection.json();
  if (connection.ok) {
    console.log(imgData);
    imgBox.src = imgData["profileImg"];
  }
}

// Function to load session user profile logo
//window.onload = async function(){
//    console.log("logo profile session user")
//    let profileLogo = document.getElementById("loggedProfileLogo")
//    if(loggedUserName!=null){
//        fetchProfileImg(loggedUserName, profileLogo)
//    }
//}
let profileLogo = document.getElementById("loggedProfileLogo");
if (loggedUserName != null) {
  fetchProfileImg(loggedUserName, profileLogo);
}
