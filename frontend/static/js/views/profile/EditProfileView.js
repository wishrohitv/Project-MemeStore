import AbstractView from "../AbstractView.js";
import {
  apiUser,
  getUser,
  apiUserUpdateProfile,
  apiUserUpdateProfileImg,
  fetchUserInfo,
} from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.userName = params.userName[0].split("/")[0];
    this.setTitle("Edit Profile");
  }

  async getHtml() {
    try {
      if (!this.userName || getUser().userName !== this.userName) {
        this.page = document.createElement("div");
        this.page.innerHTML = "Page not found";
        return this.page;
      }

      const html = await fetch(
        "/static/js/views/profile/templates/daisyUI/editProfile.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      this.form = this.page.querySelector("form");
      this.profileImg = this.page.querySelector("#selectedProfileImg");
      this.name_ = this.page.querySelector("#uName");
      this.userName = this.page.querySelector("#userName");
      this.bio = this.page.querySelector("#bio");
      this.previewBox = this.page.querySelector("#profilePreview");

      // imgUploadButton
      this.imgUploadButtonBox = this.page.querySelector("#imgUploadButton");
      this.imgUploadButtonBox.addEventListener(
        "click",
        this.imgUploadButton.bind(this),
      );
      // Currently selected profile image by user
      this.selectedInputFile = this.page.querySelector("#selectedProfileImg");
      this.selectedInputFile.addEventListener(
        "change",
        this.loadFile.bind(this),
      );
      // Profile data
      this.form.addEventListener("submit", (e) => {
        e.preventDefault();
        this.updateProfile();
      });

      this.fetchUserProfileData();
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading profile edit page";
    }

    return this.page;
  }

  loadFile(event) {
    let previewBox = this.previewBox;
    let imgUploadButtonBox = this.imgUploadButtonBox;
    let reader = new FileReader();
    reader.onload = function () {
      let fileName = event.target.files[0].type;
      // show img upload button
      imgUploadButtonBox.classList.remove("hidden");
      previewBox.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
  }
  // function to fetch user's profile data
  async fetchUserProfileData() {
    try {
      let connection = await fetch(`${apiUser}/${getUser().userName}`, {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
      });
      let res = await connection.json();
      if (connection.status === 200) {
        this.name_.value = res.payload.name;
        this.userName.value = res.payload.userName;
        this.bio.value = res.payload.bio;
        this.previewBox.src = res.payload.profileImgUrl;
        this.user = res.payload;
      } else {
        console.error(res);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async imgUploadButton() {
    let formData = new FormData();
    for (const file of this.selectedInputFile.files) {
      formData.append("file", file, file.name);
    }

    try {
      let connection = await fetch(apiUserUpdateProfileImg, {
        method: "PUT",
        credentials: "include",
        body: formData,
      });
      let re = await connection.json();
      if (connection.ok) {
        this.imgUploadButtonBox.classList.add("hidden");
      } else {
        console.error(re);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async updateProfile() {
    let isModified = false;
    let formData = new FormData();
    if (this.user.name !== this.name_.value) {
      formData.append("name", this.name_.value);
      isModified = true;
    }
    if (this.user.userName !== this.userName.value) {
      formData.append("userName", this.userName.value);
      isModified = true;
    }
    if (this.user.bio !== this.bio.value) {
      formData.append("bio", this.bio.value);
      isModified = true;
    }
    const data = Object.fromEntries(formData.entries()); // Convert form to simple object
    if (!isModified) {
      return;
    }
    try {
      let res = await fetch(apiUserUpdateProfile, {
        method: "PUT",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      let re = await res.json();
      if (res.ok) {
        this.imgUploadButtonBox.classList.add("hidden");
        console.log(re);
      } else {
        console.error(re);
      }
    } catch (e) {
      console.error(e);
    }
  }
}
