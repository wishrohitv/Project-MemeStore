import AbstractView from "../AbstractView.js";
import { initializeTemplate, apiHomeFeed } from "../../utils/base.js";
import { postCard } from "../../utils/postCard.js";

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
      throw new Error(error);
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
        feedData.forEach(async (post) => {
          const clone = postTemplate.content.cloneNode(true);
          let card = await postCard(clone, post, {
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
      this.spinner.classList.add("hidden");
    });
  }
}
