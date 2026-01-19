let form = document.querySelector("form");
let profileImg = document.getElementById("selectedProfileImg");
let name_ = document.getElementById("uName");
let userName = document.getElementById("userName");
let bio = document.getElementById("bio");

// imgUploadButton
let imgUploadButtonBox = document.getElementById("imgUploadButton");
// Currently selected profile image by user
let selectedInputFile = document.getElementById("selectedProfileImg");

// function to fetch user's profile data
async function fetchUserProfileData() {
  try {
    let connection = await fetch(`${apiUser}/${loggedUserName}`, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    });
    let res = await connection.json();

    console.log(res);
    name_.value = res.payload.name;
    userName.value = res.payload.userName;
    bio.value = res.payload.bio;
    profileImg.src = res.payload.profileImgUrl;
  } catch (e) {
    console.error(e);
  }
}

let previewBox = document.getElementById("profilePreview");
var loadFile = function (event) {
  var reader = new FileReader();
  reader.onload = function () {
    let fileName = event.target.files[0].type;
    //    if(fileName==="image/png"){
    //      previewBox.src = reader.result;
    //    }else {
    //        console.error("Unsupported file type")
    //    }
    // show img upload button
    imgUploadButtonBox.classList.remove("hidden");
    previewBox.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
};

async function imgUploadButton() {
  let data = new FormData();
  console.log(selectedInputFile.files[0]);
  for (const file of selectedInputFile.files) {
    data.append("files", file, file.name);
    data.append("userName", userName.value);
  }
  console.log(data);
  try {
    let res = await fetch(apiUserUpdateProfileImg, {
      method: "PUT",
      credentials: "include",
      body: data,
    });
    let re = await res.json();
    if (res.ok) {
      imgUploadButtonBox.classList.remove("hidden");
    }
    console.log(re);
  } catch (e) {
    console.error(e);
  }
}
// Profile data
form.addEventListener("submit", (e) => {
  e.preventDefault();
  updateProfile();
});
async function updateProfile() {
  let data = new FormData();
  data.append("name", name_.value);
  data.append("userName", userName.value);
  data.append("bio", bio.value);
  data.append("uid", loggedUserUid);
  try {
    let res = await fetch(apiUserUpdateProfile, {
      method: "PUT",
      credentials: "include",
      body: data,
    });
    let re = await res.json();
    if (res.ok) {
      imgUploadButtonBox.classList.remove("hidden");
    }
    console.log(re);
  } catch (e) {
    console.error(e);
  }
}

function router() {
  const path = location.pathname;
  const paths = path.split("/");
  // ['', 'user', 'pmModi', "edit]
  if (
    paths[1] === "user" &&
    loggedUserName === paths[2] &&
    paths[3] === "edit"
  ) {
    fetchUserProfileData(paths[2]);
    fetchProfileImg(paths[2], profileImg);
  } else {
    window.location.href = "/404";
  }
}

function navigate(url) {
  history.pushState({}, "", url);
  router();
}

window.addEventListener("popstate", router);
router();

window.onload = async function () {
  await fetchUserProfileData();
  manageNavbar();
};
