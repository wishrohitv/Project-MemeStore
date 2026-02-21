import AbstractView from "../AbstractView.js";
import {
  apiUserPostsFeed,
  apiPostsReplies,
  initializeTemplate,
} from "../../utils/base.js";

import { postCard } from "../../macroComponets/postCard.js";
import { replieCard } from "../../macroComponets/replieCard.js";

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
      this.postContainer = this.page.querySelector(".postCard");
      this.repliesContainer = this.page.querySelector("#repliesContainer");
      this.replieInputContainer = this.page.querySelector(
        "#replieInputContainer",
      );
      this.spinner = this.page.querySelector("#spinner");
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
      this.spinner.classList.remove("hidden");
      initializeTemplate({}).then(async (postTemplate) => {
        /// Fetch home feed data
        const connection = await fetch(`${apiUserPostsFeed}/${this.postID}`, {
          credentials: "include",
        });

        const response = await connection.json();
        if (connection.ok) {
          const post = response.payload[0];
          const clone = postTemplate.content.cloneNode(true);
          this.setTitle(post.title ?? post.userName);
          const card = await postCard(clone, post, {
            type: "post",
            parentCardClbk: (parentPostID) => {
              this.navigator("/post/" + parentPostID);
            },
          });
          this.postContainer.appendChild(card);
          this.spinner.classList.add("hidden");
          // Add replie imput card
          this.replieInputContainer.appendChild(await replieCard(this.postID));
          if (connection.status !== 404) {
            if (post.replieCount !== 0) {
              this.fetchPostReplies();
            }
          }
        } else {
          console.error(response);
          this.spinner.classList.add("hidden");
        }
      });
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
          let card = await postCard(clone, post, {
            mainCardClbk: (postID) => {
              this.navigator("/post/" + postID);
            },
            parentCardClbk: (parentPostID) => {
              this.navigator("/post/" + parentPostID);
            },
          });

          this.repliesContainer.appendChild(card);
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
