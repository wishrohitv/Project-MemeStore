import AbstractView from "../AbstractView.js";
import {
  initializeTemplate,
  apiHomeFeed,
  apiTogglePostLike,
  apiTogglePostBookmark,
  apiGetPostMedia,
} from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("MemeStore");
  }

  async getHtml(navigator) {
    this.navigator = navigator;
    try {
      const html = await fetch(
        "./static/js/views/home/templates/daisyUI/home.html",
      );

      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;
      // Container of post preview
      this.postContainer = this.page.querySelector("#postContainer");
      // Spinner
      this.spinner = this.page.querySelector("#spinner");

      // Fetch home feed
      this.loadHomeFeed();
    } catch (error) {
      console.error("Error fetching HTML:", error);
      this.page = "<h1>Error</h1><p>Failed to load page</p>";
    }
    return this.page;
  }

  // Function to fetch home feed for user
  async fetchHomeFeed() {
    let connection = await fetch(apiHomeFeed, {
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

  async loadHomeFeed() {
    this.spinner.classList.remove("hidden");
    initializeTemplate({}).then(async (postTemplate) => {
      /// Fetch home feed data
      const feedData = await this.fetchHomeFeed();
      // Check if feedData is not empty
      if (feedData) {
        // postTemplate comming from base.js
        // Loop feedData list
        feedData.forEach((post) => {
          const clone = postTemplate.content.cloneNode(true);
          clone.querySelector(".card").addEventListener("click", (e) => {
            if (
              e.target.closest(
                "a, button, .likeBtn, .bookmarkBton, .shareBtn, .downloadBtn, #moreBtnContainer",
              )
            )
              return;
            this.navigator("/post/" + post.postID);
          });
          clone.querySelector(".cardTitle").textContent = post.title;
          clone.querySelector(".cardInfo").textContent = post.tags;
          clone.querySelector(".postUserName").textContent = post.userName;
          if (post.fileType === "image") {
            clone.querySelector(".postContentImgPreview").src =
              post.postMediaUrl;
          } else if (post.fileType === "video") {
            clone
              .querySelector(".postContentImgPreview")
              .classList.add("hidden");
            clone
              .querySelector(".postContentVidPreview")
              .classList.remove("hidden");
            clone.querySelector(".postContentVidPreview").src =
              post.postMediaUrl;
          }
          clone.querySelector(".postUserPic").src = post.postUserPicUrl;
          // Post like
          const likeBtn = clone.querySelector(".likeBtn");
          if (post.likeCount !== 0) {
            likeBtn.querySelector(".count").innerText = post.likeCount;
          }

          if (post.isLiked) {
            likeBtn.querySelector(".svgs").children[0].classList.add("hidden");
            likeBtn
              .querySelector(".svgs")
              .children[1].classList.remove("hidden");
          }
          likeBtn
            .querySelector(".svgs")
            .addEventListener("click", async (event) => {
              try {
                let conn = await fetch(`${apiTogglePostLike}/${post.postID}`, {
                  method: "PUT",
                  credentials: "include",
                });
                let res = await conn.json();
                if (conn.ok) {
                  if (res.isLiked) {
                    event.target.parentNode.parentNode.children[1].classList.remove(
                      "hidden",
                    );
                    event.target.parentNode.parentNode.children[0].classList.add(
                      "hidden",
                    );
                    likeBtn.querySelector(".count").innerText =
                      post.likeCount + 1;
                  } else {
                    event.target.parentNode.parentNode.children[1].classList.add(
                      "hidden",
                    );
                    event.target.parentNode.parentNode.children[0].classList.remove(
                      "hidden",
                    );
                    likeBtn.querySelector(".count").innerText =
                      post.likeCount - 1;
                  }
                }
                console.log(res);
              } catch (e) {
                console.error(e);
              }
            });
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
            .addEventListener("click", async (event) => {
              try {
                let conn = await fetch(
                  `${apiTogglePostBookmark}/${post.postID}`,
                  {
                    method: "PUT",
                    credentials: "include",
                  },
                );
                let res = await conn.json();
                if (conn.ok) {
                  if (res.isBookmarked) {
                    event.target.parentNode.parentNode.children[1].classList.remove(
                      "hidden",
                    );
                    event.target.parentNode.parentNode.children[0].classList.add(
                      "hidden",
                    );
                    bookmarkBtn.querySelector(".count").innerText =
                      post.bookmarkCount + 1;
                  } else {
                    event.target.parentNode.parentNode.children[1].classList.add(
                      "hidden",
                    );
                    event.target.parentNode.parentNode.children[0].classList.remove(
                      "hidden",
                    );
                    bookmarkBtn.querySelector(".count").innerText =
                      post.bookmarkCount - 1;
                  }
                }
                console.log(res);
              } catch (e) {
                console.error(e);
              }
            });
          // Download Button
          const downloadBtn = clone.querySelector(".downloadBtn");
          downloadBtn.addEventListener("click", (e) => {
            window.location.href = `${apiGetPostMedia}/${post.postID}`;
            // Good for showing ads
            // window.open(
            //   `${apiGetPostMedia}/${post.postID}`,
            //   "_blank",
            // );
          });
          // Link of creator's profile
          clone.querySelector(".postUserPic").src = post.profileImgUrl;
          clone.querySelector(".postUserName").href = `/user/${post.userName}`;
          clone.querySelector(".userProfileLink").href =
            `/user/${post.userName}`;

          this.postContainer.appendChild(clone);
        });
      } else {
        console.error(feedData);
      }
      this.spinner.classList.add("hidden");
    });
  }

  // // Fetch home feed on page load
  // window.addEventListener("load", async (e) => {
  //   spinner.classList.remove("hidden");
  //   loadHomeFeed();
  //   spinner.classList.add("hidden");
  // });
}
