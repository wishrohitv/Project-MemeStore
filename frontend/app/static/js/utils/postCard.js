import {
  initializeTemplate,
  apiTogglePostLike,
  apiTogglePostBookmark,
  apiGetPostMedia,
  apiUserPostsFeed,
} from "./base.js";
import { formatDate } from "./datetime.js";

export async function postCard(clone, post, { type = "feed" }) {
  // If type = feed it means card is used for home feed and type = post so customize it for post screen
  if (!(type === "feed" || type === "post"))
    throw Error(`Invalid type used ${type}`);
  if (type === "feed") {
    clone.querySelector(".card").addEventListener("click", (e) => {
      if (
        e.target.closest(
          "a, button, .likeBtn, .bookmarkBtn, .shareBtn, .downloadBtn, #moreBtnContainer",
        )
      )
        return;
      this.navigator("/post/" + post.postID);
    });
  } else {
    // Post page specific actions
    // this.setTitle(post.title ?? post.userName);
  }
  clone.querySelector(".qoute").addEventListener("click", (e) => {
    this.navigator("/post/create?reqouteTo=" + post.postID);
  });
  clone.querySelector(".cardTitle").textContent = post.title;
  clone.querySelector(".cardInfo").textContent = post.tags;
  clone.querySelector(".postUserName").textContent = post.userName;
  clone.querySelector(".postUserPic").src = post.postUserPicUrl;

  if (post.fileType) {
    clone.querySelector(".media").classList.remove("hidden");
    if (post.fileType === "image") {
      clone.querySelector(".postContentImgPreview").src = post.postMediaUrl;
    } else if (post.fileType === "video") {
      clone.querySelector(".postContentImgPreview").classList.add("hidden");
      clone.querySelector(".postContentVidPreview").classList.remove("hidden");
      clone.querySelector(".postContentVidPreview").src = post.postMediaUrl;
    }
  }
  // Post like
  const likeBtn = clone.querySelector(".likeBtn");
  if (post.likeCount !== 0) {
    likeBtn.querySelector(".count").innerText = post.likeCount;
  }

  if (post.replieCount !== 0) {
    clone.querySelector(".replieCount").innerText =
      post.replieCount + " replies";
  }

  if (post.isLiked) {
    clone.querySelector("[data-unliked]").classList.add("hidden");
    clone.querySelector("[data-liked]").classList.remove("hidden");
  }
  likeBtn.querySelector(".svgs").addEventListener("click", async (event) => {
    try {
      let conn = await fetch(`${apiTogglePostLike}/${post.postID}`, {
        method: "PUT",
        credentials: "include",
      });
      let res = await conn.json();
      if (conn.ok) {
        const e = event.target.parentNode.parentNode;
        const liked = e.querySelector("[data-liked]");
        const unliked = e.querySelector("[data-unliked]");
        if (res.isLiked) {
          liked.classList.remove("hidden");
          unliked.classList.add("hidden");
          likeBtn.querySelector(".count").innerText = post.likeCount
            ? post.likeCount
            : post.likeCount + 1;
        } else {
          liked.classList.add("hidden");
          unliked.classList.remove("hidden");
          likeBtn.querySelector(".count").innerText = post.isLiked
            ? post.likeCount - 1
            : post.likeCount;
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
    clone.querySelector("[data-unbookmarked]").classList.add("hidden");
    clone.querySelector("[data-bookmarked]").classList.remove("hidden");
  }
  bookmarkBtn
    .querySelector(".svgs")
    .addEventListener("click", async (event) => {
      try {
        let conn = await fetch(`${apiTogglePostBookmark}/${post.postID}`, {
          method: "PUT",
          credentials: "include",
        });
        let res = await conn.json();
        if (conn.ok) {
          const e = event.target.parentNode.parentNode;
          const bookmarked = e.querySelector("[data-bookmarked]");
          const unbookmarked = e.querySelector("[data-unbookmarked]");
          if (res.isBookmarked) {
            bookmarked.classList.remove("hidden");
            unbookmarked.classList.add("hidden");
            bookmarkBtn.querySelector(".count").innerText = post.isBookmarked
              ? post.bookmarkCount
              : post.bookmarkCount + 1;
          } else {
            bookmarked.classList.add("hidden");
            unbookmarked.classList.remove("hidden");
            bookmarkBtn.querySelector(".count").innerText = post.isBookmarked
              ? post.bookmarkCount - 1
              : post.bookmarkCount;
          }
        }
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
  clone.querySelector(".createdAt").innerText = formatDate(post.createdAt);

  // Load parent post
  if (post.parentPostID) {
    const connection = await fetch(`${apiUserPostsFeed}/${post.parentPostID}`, {
      credentials: "include",
    });
    let parentPostObj = await connection.json();

    if (connection.ok) {
      const parentPost = parentPostObj.payload[0];
      let parentPostContainer = clone.querySelector(".parentPostContainer");
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
        if (parentPost.fileType) {
          cloneParentMacro.querySelector(".media").classList.remove("hidden");
          if (parentPost.fileType === "image") {
            cloneParentMacro.querySelector(".postContentImgPreview").src =
              parentPost.postMediaUrl;
          } else if (parentPost.fileType === "video") {
            cloneParentMacro
              .querySelector(".postContentImgPreview")
              .classList.add("hidden");
            cloneParentMacro
              .querySelector(".postContentVidPreview")
              .classList.remove("hidden");
            cloneParentMacro.querySelector(".postContentVidPreview").src =
              parentPost.postMediaUrl;
          }
        }
        cloneParentMacro.querySelector(".cardTitle").textContent =
          parentPost.title;
        cloneParentMacro.querySelector(".postUserName").textContent =
          parentPost.userName;
        cloneParentMacro.querySelector(".userProfileLink").href =
          `/user/${parentPost.userName}`;
        cloneParentMacro.querySelector(".postUserPic").src =
          parentPost.profileImgUrl;
        cloneParentMacro.querySelector(".createdAt").innerText = formatDate(
          parentPost.createdAt,
        );

        parentPostContainer.appendChild(cloneParentMacro);
      }
    }
  }
  return clone;
}
