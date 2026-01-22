import AbstractView from "../AbstractView.js";
import {
  apiUser,
  getUser,
  apiUserPostsFeed,
  initializeTemplate,
  apiAddFollower,
  apiRemoveFollower,
} from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.userName = params.userName[0];
    this.setTitle("Profile");
  }

  async getHtml() {
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
      this.goToEditBtn = this.page.querySelector("#goToEdit");
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
        console.log(res);
        if (getUser().id === res.payload.id) {
          console.log(typeof res.payload.id);
          console.log("profile id", uid.value, " session id: ", getUser()?.id);
          this.followerBtn.disabled = true;
          this.goToEditBtn.href = `/edit/profile/${res.payload.userName}`;
          this.goToEditBtn.classList.remove("hidden");
        } else if (res.payload.isFollowing) {
          this.followerBtn.innerText = "Unfollow";
          this.followerBtn.classList.remove("bg-purple-500");
          this.followerBtn.classList.remove("hover:bg-purple-600");
          this.followerBtn.classList.add("bg-red-400");
          this.followerBtn.classList.add("hover:bg-red-500");
        } else {
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
        return res.error;
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
      const postTemplate = await initializeTemplate();
      // Loop feedData list
      feedData.forEach((post) => {
        const clone = postTemplate.content.cloneNode(true);
        clone.querySelector(".cardTitle").textContent = post.title;
        clone.querySelector(".cardInfo").textContent = post.tags;
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
        // Post like
        const likeBtn = clone.querySelector(".likeButton");
        if (post.likeCount !== 0) {
          likeBtn.querySelector(".count").innerText = post.likeCount;
        }

        if (post.isLiked) {
          likeBtn.querySelector(".svgs").children[0].classList.add("hidden");
          likeBtn.querySelector(".svgs").children[1].classList.remove("hidden");
        }
        likeBtn
          .querySelector(".svgs")
          .addEventListener("click", (event) =>
            togglePostLike(post.postID, event),
          );
        // Post Bookmark
        console.log(post);
        const bookmarkBtn = clone.querySelector(".bookmarkBtn");
        if (post.bookmarkCount !== 0) {
          bookmarkBtn.querySelector(".count").innerText = post.bookmarkCount;
        }

        if (post.isBookmarked) {
          bookmarkBtn
            .querySelector(".svgs")
            .children[0].classList.add("hidden");
          bookmarkBtn
            .querySelector(".svgs")
            .children[1].classList.remove("hidden");
        }
        bookmarkBtn
          .querySelector(".svgs")
          .addEventListener("click", (event) =>
            togglePostLike(post.postID, event),
          );
        // Link of creator's profile
        clone.querySelector(".postUserPic").src = post.profileImgUrl;
        clone.querySelector(".postUserName").href = `/user/${post.userName}`;
        clone.querySelector(".userProfileLink").href = `/user/${post.userName}`;

        this.postContainer.appendChild(clone);
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
