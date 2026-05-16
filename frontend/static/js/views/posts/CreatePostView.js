import AbstractView from "../AbstractView.js";
import { apiUploadPosts, flash } from "../../utils/base.js";
import { parseUrlParams } from "../../utils/parseUrlParams.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Create Post");
    this.reqouteTo = parseUrlParams().reqouteTo;
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/posts/templates/daisyUI/createPosts.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      // Form
      this.form = this.page.querySelector("form");
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
      // Post age rating
      this.postAgeRating = this.page.querySelector("#ageRating");
      // Post visibility
      this.postCategory = this.page.querySelector("#category");
      this.currentSelectedFile.addEventListener(
        "change",
        this.loadFile.bind(this),
      );
      this.page
        .querySelector("form")
        .addEventListener("submit", this.uploadPostOnServer.bind(this));
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading Create post page";
    }

    return this.page;
  }

  loadFile(event) {
    var reader = new FileReader();
    const previewBox = this.previewBox;
    const page = this.page;
    reader.onload = function () {
      let fileName = event.target.files[0].type;
      if (
        fileName === "image/png" ||
        fileName === "image/gif" ||
        fileName === "image/jpeg"
      ) {
        previewBox[0].classList.remove("hidden");
        previewBox[1].classList.add("hidden");
      } else if (fileName === "video/mp4") {
        previewBox[1].classList.remove("hidden");
        previewBox[0].classList.add("hidden");
      }
      let imgPreview = page.querySelector("#imgPreview");
      let vidPreview = page.querySelector("#vidPreview");
      imgPreview.src = reader.result;
      vidPreview.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
  }

  async uploadPostOnServer(event) {
    event.preventDefault();
    let postForm = new FormData(this.form);
    postForm.append(
      "ageRating",
      this.postAgeRating.selectedOptions[0].innerText,
    );
    postForm.append("category", this.postCategory.selectedOptions[0].innerText);
    const data = Object.fromEntries(postForm.entries()); // Convert form to simple object

    // for (const file of this.currentSelectedFile.files) {
    //   Can be used for multiple file upload
    //   postForm.append("files", file, file.name);
    //   postForm.append("postTitle", this.postTitle.value);
    //   postForm.append("postTags", this.postTags.value);
    // }

    try {
      let _apiUploadPosts = apiUploadPosts;
      if (this.reqouteTo) {
        _apiUploadPosts += `?parentPostID=${this.reqouteTo}`;
      }
      let connection = await fetch(_apiUploadPosts, {
        method: "POST",
        credentials: "include",
        body: postForm,
      });
      let res = await connection.json();
      if (connection.ok) {
        console.log("uploaded successfully");
      } else {
        flash("Failed to upload post", { messageType: "error" });
        console.error("failed to upload", res);
      }
    } catch (e) {
      console.error(e);
    }
  }
}
