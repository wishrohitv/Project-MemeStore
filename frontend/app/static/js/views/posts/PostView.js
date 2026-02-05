import AbstractView from "../AbstractView.js";
import {
  apiUserPostsFeed,
  apiPostsReplies,
  initializeTemplate,
  apiTogglePostLike,
  apiTogglePostBookmark,
} from "../../utils/base.js";
import { formatDate } from "../../utils/datetime.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.postID = params.postID[0];
    this.setTitle("Post");
  }

  async getHtml(navigator) {
    this.navigator = navigator;
    try {
      const html = await fetch(
        "/static/js/views/posts/templates/daisyUI/posts.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;
      this.repliesContainer = this.page.querySelector("#repliesContainer");
      this.form = this.page.querySelector("#commentForm");
      this.form.addEventListener("submit", async (e) => {
        e.preventDefault();
        this.createComment();
      });
      this.fetchPost();
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading Create post page";
    }

    return this.page;
  }

  async fetchPost() {
    try {
      const connection = await fetch(`${apiUserPostsFeed}/${this.postID}`, {
        credentials: "include",
      });

      const response = await connection.json();
      const post = response.payload[0];
      if (connection.ok) {
        const clone = this.page;
        clone.querySelector(".qoute").addEventListener("click", (e) => {
          this.navigator("/post/create");
        });
        this.setTitle(post.title ?? post.userName);
        clone.querySelector(".cardTitle").textContent = post.title;
        clone.querySelector(".cardInfo").textContent = post.tags;
        clone.querySelector(".postUserName").textContent = post.userName;

        if (post.fileType) {
          clone.querySelector(".media").classList.remove("hidden");
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
        }
        // Post like
        const likeBtn = clone.querySelector(".likeBtn");
        if (post.likeCount !== 0) {
          likeBtn.querySelector(".count").innerText = post.likeCount;
        }

        if (post.isLiked) {
          likeBtn.querySelector(".svgs").children[0].classList.add("hidden");
          likeBtn.querySelector(".svgs").children[1].classList.remove("hidden");
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
        clone.querySelector(".userProfileLink").href = `/user/${post.userName}`;
        clone.querySelector(".createdAt").innerText = formatDate(
          post.createdAt,
        );

        // Load parent post
        if (post.parentPostID) {
          const connection = await fetch(
            `${apiUserPostsFeed}/${post.parentPostID}`,
            {
              credentials: "include",
            },
          );
          let parentPostObj = await connection.json();

          if (connection.ok) {
            const parentPost = parentPostObj.payload[0];
            let parentPostContainer = clone.querySelector(
              ".parentPostContainer",
            );
            if (parentPostContainer) {
              parentPostContainer.classList.remove("hidden");
              const parentMacro = await initializeTemplate({
                macro: "parent",
              });
              const cloneParentMacro = parentMacro.content.cloneNode(true);
              cloneParentMacro
                .querySelector(".card")
                .addEventListener("click", (e) => {
                  if (e.target.closest(".card")) {
                    this.navigator("/post/" + parentPost.postID);
                  }
                });
              cloneParentMacro.querySelector(".cardTitle").textContent =
                parentPost.title;
              cloneParentMacro.querySelector(".postUserName").textContent =
                parentPost.userName;
              cloneParentMacro.querySelector(".userProfileLink").href =
                `/user/${parentPost.userName}`;
              cloneParentMacro.querySelector(".postUserPic").src =
                parentPost.profileImgUrl;
              cloneParentMacro.querySelector(".createdAt").innerText =
                formatDate(parentPost.createdAt);

              parentPostContainer.appendChild(cloneParentMacro);
            }
          }
        }
      }
      if (connection.status !== 404) {
        if (post.replieCount !== 0) {
          this.fetchPostReplies();
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  async fetchPostReplies() {
    const connection = await fetch(`${apiPostsReplies}/${this.postID}`, {
      credentials: "include",
    });

    const posts = await connection.json();
    if (connection.ok) {
      initializeTemplate({}).then(async (postTemplate) => {
        /// Fetch home feed data
        // Loop posts list
        posts.payload.forEach(async (post) => {
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
          clone.querySelector(".qoute").addEventListener("click", (e) => {
            this.navigator("/post/create");
          });
          clone.querySelector(".cardTitle").textContent = post.title;
          clone.querySelector(".cardInfo").textContent = post.tags;
          clone.querySelector(".postUserName").textContent = post.userName;

          if (post.fileType) {
            clone.querySelector(".media").classList.remove("hidden");
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
          }
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
          clone.querySelector(".createdAt").innerText = formatDate(
            post.createdAt,
          );

          // Load parent post
          if (post.parentPostID) {
            const connection = await fetch(
              `${apiUserPostsFeed}/${post.parentPostID}`,
              {
                credentials: "include",
              },
            );
            let parentPostObj = await connection.json();

            if (connection.ok) {
              const parentPost = parentPostObj.payload[0];
              let parentPostContainer = clone.querySelector(
                ".parentPostContainer",
              );
              if (parentPostContainer) {
                parentPostContainer.classList.remove("hidden");
                const parentMacro = await initializeTemplate({
                  macro: "parent",
                });
                const cloneParentMacro = parentMacro.content.cloneNode(true);
                cloneParentMacro
                  .querySelector(".card")
                  .addEventListener("click", (e) => {
                    if (e.target.closest(".card")) {
                      this.navigator("/post/" + parentPost.postID);
                    }
                  });
                cloneParentMacro.querySelector(".cardTitle").textContent =
                  parentPost.title;
                cloneParentMacro.querySelector(".postUserName").textContent =
                  parentPost.userName;
                cloneParentMacro.querySelector(".userProfileLink").href =
                  `/user/${parentPost.userName}`;
                cloneParentMacro.querySelector(".postUserPic").src =
                  parentPost.profileImgUrl;
                cloneParentMacro.querySelector(".createdAt").innerText =
                  formatDate(parentPost.createdAt);

                parentPostContainer.appendChild(cloneParentMacro);
              }
            }
          }

          this.repliesContainer.appendChild(clone);
        });
      });
    }
  }

  async createComment() {
    const formData = new FormData(this.form);
    const data = Object.fromEntries(formData.entries());
    const connection = await fetch(`${apiCreateComment}/${this.postID}`, {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(data),
    });

    connection.ok && this.fetchPostReplies();
  }
}
