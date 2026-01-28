import AbstractView from "../AbstractView.js";
import {
  apiUserPostsFeed,
  apiComments,
  apiCreateComment,
  apiUpdateComments,
  apiDeleteComment,
} from "../../utils/base.js";

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
      this.commentsContainer = this.page.querySelector("#commentsContainer");
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
    console.log("Fetching post");
    try {
      const connection = await fetch(`${apiUserPostsFeed}/${this.postID}`, {
        credentials: "include",
      });

      const response = await connection.json();
      const post = response.payload[0];
      if (connection.ok) {
        const clone = this.page;
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
      }
      if (connection.status !== 404) {
        this.fetchComments();
      }
    } catch (e) {
      console.error(e);
    }
  }

  async fetchComments() {
    const connection = await fetch(`${apiComments}/${this.postID}`, {
      credentials: "include",
    });

    const commetnsObj = await connection.json();

    if (connection.ok) {
      commetnsObj.payload.forEach((comment) => {
        this.commentsContainer.innerHTML += this.commentUser(
          comment.commentID,
          comment.userName,
          comment.profileImgUrl,
          comment.content,
        );
      });
    }
  }

  commentUser(commentID, userName, profileImgUrl, content) {
    return `<div class="flex flex-col">
        <!-- User info -->
        <input type="hidden" value="${commentID}" />
        <div class="flex flex-row justify-between">
            <div class="flex flex-row items-center gap-2">
                <img
                    class="size-10 rounded-full bg-blue-500"
                    src="${profileImgUrl}"
                />
                <div>${userName}</div>
                <div class="text-neutral-500">2 hour ago</div>
            </div>
            <!-- More option button -->
            <div class="dropdown dropdown-end">
                <div tabindex="0" role="button" class="">
                    <svg
                        class="hover:scale-120 hover:cursor-pointer"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="lucide lucide-ellipsis-vertical-icon lucide-ellipsis-vertical"
                    >
                        <circle cx="12" cy="12" r="1" />
                        <circle cx="12" cy="5" r="1" />
                        <circle cx="12" cy="19" r="1" />
                    </svg>
                    More
                </div>
                <ul
                    tabindex="0"
                    class="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow"
                >
                    <li>
                        <a data-link>
                            Delete
                        </a>
                    </li>
                    <li><a data-link>Report</a></li>
                    <li><a data-link>Block User</a></li>
                </ul>
            </div>
        </div>
        <!-- Text -->
        <div class="flex flex-row">
            <div class="w-16"></div>
            <div class="">${content}</div>
        </div>
    </div>`;
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

    connection.ok && this.fetchComments();
  }
}
