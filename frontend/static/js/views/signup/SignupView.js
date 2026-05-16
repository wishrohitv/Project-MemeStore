import AbstractView from "../AbstractView.js";
import { apiSignupUser } from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("signup");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/signup/templates/daisyUI/signup.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      this.form = this.page.querySelector("#signupForm");

      this.form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Stop the page from reloading

        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries()); // Convert form to simple object
        await this.signup(data);
      });
    } catch (error) {
      console.error("Error fetching HTML:", error);
      this.page = "<h1>Error</h1><p>Failed to signup page</p>";
    }
    return this.page;
  }

  async signup(data) {
    try {
      const connection = await fetch(apiSignupUser, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const response = await connection.json();
      if (connection.status === 201) {
        window.location.href = "/auth/login";
      } else {
        console.error("Signup failed", response);
      }
    } catch (e) {
      console.error("Signup failed : ", e);
    }
  }
}
