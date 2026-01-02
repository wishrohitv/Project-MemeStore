console.log("createPost.js loaded");

// Preview box
let previewBox = document.getElementsByClassName("previewBox")[0].children;

// Current selected file
let currentSelectedFIle = document.getElementById("currentSelectedFile");
// Post title
let postTitle = document.getElementById("postTitle");
// Post tags
let postTags = document.getElementById("postTags");
// Post visibility
let postVisibility = document.getElementsByName("visibility");
// Post age rating
let postAgeRating = document.getElementById("ageRating");
// Post visibility
let postCategory = document.getElementById("category");

var loadFile = function (event) {
  var reader = new FileReader();
  reader.onload = function () {
    let fileName = event.target.files[0].type;
    if (fileName === "image/png") {
      previewBox[0].classList.remove("hidden");
      previewBox[1].classList.add("hidden");
    } else if (fileName === "video/mp4") {
      previewBox[1].classList.remove("hidden");
      previewBox[0].classList.add("hidden");
    }
    var imgPreview = document.getElementById("imgPreview");
    var vidPreview = document.getElementById("vidPreview");
    imgPreview.src = reader.result;
    vidPreview.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
};

async function uploadPostOnServer() {
  let postForm = new FormData();
  var reader = new FileReader();
  console.log(reader.result);
  for (const file of currentSelectedFIle.files) {
    postForm.append("files", file, file.name);
    postForm.append("postTitle", postTitle.value);
    postForm.append("postTags", postTags.value);
    postForm.append("postVisibility", postVisibility[0].checked); // Here we checking only public radio tag between public and private class
    postForm.append("ageRating", postAgeRating.selectedOptions[0].innerText);
    postForm.append("category", postCategory.selectedOptions[0].innerText);
  }

  try {
    let connection = await fetch(apiUploadPosts, {
      method: "POST",
      credentials: "include",
      body: postForm,
    });
    let res = await connection.json();
    if (connection.ok) {
      console.log("uploaded successfully");
    } else {
      console.error("failed to upload", res);
    }
  } catch (e) {
    console.error(e);
  }
}
