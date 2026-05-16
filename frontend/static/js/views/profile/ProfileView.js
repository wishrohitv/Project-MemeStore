import AbstractView from "../AbstractView.js";
import {
  apiUser,
  getUser,
  apiUserPostsFeed,
  initializeTemplate,
  apiAddFollower,
  apiRemoveFollower,
} from "../../utils/base.js";

import { postCard } from "../../macroComponets/postCard.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.userName = params.userName[0];
    this.setTitle("Profile");
  }

  async getHtml(navigator) {
    this.navigator = navigator;
    try {
      const html = await fetch(
        "/static/js/views/profile/templates/daisyUI/profile.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      this.profileImg = this.page.querySelector("#profileImg");
      this.followerCount = this.page.querySelector("#followerCount");
      this.followingCount = this.page.querySelector("#followingCount");
      this.name_ = this.page.querySelector("#uName");
      this.userName_ = this.page.querySelector("#userName");
      this.bio = this.page.querySelector("#bio");
      this.uid = this.page.querySelector("#uid");
      this.followerBtn = this.page.querySelector("#followerBtn");
      this.goToEditBtn = this.page.querySelector("#goToEditBtn");
      this.blockBtn = this.page.querySelector("#blockBtn");
      this.reportUserBtn = this.page.querySelector("#reportUserBtn");
      this.spinnerProfile = this.page.querySelector("#spinnerProfile");
      this.userProfileContainer = this.page.querySelector(
        "#userProfileContainer",
      );
      // Container of post preview
      this.postContainer = this.page.querySelector("#userPostContainer");
      this.followerBtn.addEventListener("click", this.addFollower.bind(this));
      this.fetchUserProfileData(this.userName);
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading login page";
    }

    return this.page;
  }

  // function to fetch user's profile data
  async fetchUserProfileData(userName) {
    this.spinnerProfile.classList.remove("hidden");
    try {
      const connection = await fetch(`${apiUser}/${userName}`, {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
      });
      const res = await connection.json();
      if (connection.ok) {
        this.user = res.payload; // Declare global user variable
        this.name_.appendChild(document.createTextNode(res.payload["name"]));
        this.userName_.appendChild(
          document.createTextNode(res.payload["userName"]),
        );
        this.followerCount.innerText = `${res.payload["followerCount"]} follower`;
        this.followingCount.innerText = `${res.payload["followingCount"]} following`;
        this.uid.value = res.payload.id;
        this.bio.innerText = res.payload.bio;
        this.profileImg.src = res.payload.profileImgUrl;
        // change to followerbtn value
        const user = getUser();
        if (user && user.id === res.payload.id) {
          this.followerBtn.disabled = true;
          this.goToEditBtn.href = `/edit/profile/${res.payload.userName}`;
          this.goToEditBtn.classList.remove("hidden");
          this.blockBtn.classList.add("hidden");
          this.reportUserBtn.classList.add("hidden");
        } else if (res.payload.isFollowing) {
          this.followerBtn.innerText = "Unfollow";
          this.followerBtn.classList.remove("bg-purple-500");
          this.followerBtn.classList.remove("hover:bg-purple-600");
          this.followerBtn.classList.add("bg-red-400");
          this.followerBtn.classList.add("hover:bg-red-500");
        }

        // Load posts
        await this.loadHomeFeed(userName);
      }
    } catch (e) {
      console.error(e);
    }
    this.spinnerProfile.classList.add("hidden");
    this.userProfileContainer.classList.remove("hidden");
  }

  // Function to fetch home feed for user
  async fetchHomeFeed(userName) {
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
        return null;
      }
    } catch (error) {
      console.error(error);
      return error;
    }
  }

  async loadHomeFeed(userName) {
    /// Fetch home feed data
    const feedData = await this.fetchHomeFeed(userName);
    // Check if feedData is not empty
    if (feedData) {
      // Call postTemplate to load
      const postTemplate = await initializeTemplate({});
      // Loop feedData list
      feedData.forEach(async (post) => {
        const clone = postTemplate.content.cloneNode(true);
        const card = await postCard(clone, post, {
          mainCardClbk: (postID) => {
            this.navigator("/post/" + postID);
          },
          parentCardClbk: (parentPostID) => {
            this.navigator("/post/" + parentPostID);
          },
        });

        this.postContainer.appendChild(card);
      });
    } else {
      console.error(feedData);
    }
  }

  // Functon to addFollower
  async addFollower(event) {
    try {
      let connection = await fetch(
        this.user.isFollowing ? apiRemoveFollower : apiAddFollower,
        {
          method: this.user.isFollowing ? "DELETE" : "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json; charset=utf-8",
          },
          body: JSON.stringify({ userID: this.user.id }),
        },
      );
      let res = await connection.json();
      if (connection.ok) {
        if (res.isFollowing) {
          this.followerCount.innerText = `${this.user.followerCount + 1} follower`;
          this.followerBtn.innerText = "Unfollow";
          this.user.isFollowing = true;
          this.followerBtn.classList.remove("bg-purple-500");
          this.followerBtn.classList.remove("hover:bg-purple-600");
          this.followerBtn.classList.add("bg-red-400");
          this.followerBtn.classList.add("hover:bg-red-500");
        } else {
          this.followerCount.innerText = `${this.user.followerCount - 1} follower`;
          this.followerBtn.innerText = "Follow";
          this.user.isFollowing = false;
          this.followerBtn.classList.remove("bg-red-400");
          this.followerBtn.classList.remove("hover:bg-red-500");
          this.followerBtn.classList.add("bg-purple-500");
          this.followerBtn.classList.add("hover:bg-purple-600");
        }
      }
      console.log(res);
    } catch (error) {
      console.error(error);
    }
  }
}
