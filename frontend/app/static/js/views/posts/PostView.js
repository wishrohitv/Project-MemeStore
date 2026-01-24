import AbstractView from "../AbstractView.js";
import { apiUploadPosts } from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    console.log(params);
    this.setTitle("Post");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/posts/templates/daisyUI/posts.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      // // Form
      // this.form = this.page.querySelector("form");
      // // Preview box
      // const previewBox = this.page.querySelector(".previewBox");
      // this.previewBox = previewBox.children;
      // // Current selected file
      // this.currentSelectedFile = this.page.querySelector(
      //   "#currentSelectedFile",
      // );
      // // Post title
      // this.postTitle = this.page.querySelector("#postTitle");
      // // Post tags
      // this.postTags = this.page.querySelector("#postTags");
      // // Post age rating
      // this.postAgeRating = this.page.querySelector("#ageRating");
      // // Post visibility
      // this.postCategory = this.page.querySelector("#category");
      // this.currentSelectedFile.addEventListener(
      //   "change",
      //   this.loadFile.bind(this),
      // );
      // this.page
      //   .querySelector("form")
      //   .addEventListener("submit", this.uploadPostOnServer.bind(this));
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading Create post page";
    }

    return this.page;
  }
}
