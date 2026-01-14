import AbstractView from "../AbstractView.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Create Post");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/posts/templates/daisyUI/createPosts.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      // Preview box
      const previewBox = this.page.querySelector(".previewBox");
      this.previewBox = previewBox.children;
      // Current selected file
      this.currentSelectedFile = this.page.querySelector(
        "#currentSelectedFile",
      );
      // Post title
      this.postTitle = this.page.querySelector("#postTitle");
      // Post tags
      this.postTags = this.page.querySelector("#postTags");
      // Post visibility
      this.postVisibility = this.page.querySelector(".visibility");
      // Post age rating
      this.postAgeRating = this.page.querySelector("#ageRating");
      // Post visibility
      this.postCategory = this.page.querySelector("#category");
      this.currentSelectedFile.addEventListener("change", this.loadFile);
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading Create post page";
    }

    return this.page;
  }

  loadFile(event) {
    var reader = new FileReader();
    console.log(this.previewBox, "re");
    console.log(this.page, "re");
    reader.onload = function () {
      let fileName = event.target.files[0].type;
      if (fileName === "image/png") {
        this.previewBox[0].classList.remove("hidden");
        this.previewBox[1].classList.add("hidden");
      } else if (fileName === "video/mp4") {
        this.previewBox[1].classList.remove("hidden");
        this.previewBox[0].classList.add("hidden");
      }
      console.log(this.page, "test");
      let imgPreview = this.page.querySelector("#imgPreview");
      let vidPreview = this.page.querySelector("#vidPreview");
      imgPreview.src = reader.result;
      vidPreview.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
  }

  async uploadPostOnServer() {
    let postForm = new FormData();
    let reader = new FileReader();
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
}
