import AbstractView from "../AbstractView.js";
import { apiLoginUser, apiLogoutUser, setUser } from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Login");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/login/templates/daisyUI/login.html",
      );
      const page = await html.text();
      this.page = document.createElement("div");
      this.page.innerHTML = page;

      this.email = this.page.querySelector("#email");
      this.password = this.page.querySelector("#password");
      this.page.querySelector("form").addEventListener("submit", (e) => {
        e.preventDefault();
        this.authUser();
      });
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error loading login page";
    }

    return this.page;
  }

  async authUser() {
    try {
      let auth = await fetch(apiLoginUser, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          email: email.value,
          password: password.value,
        }),
      });
      let res = await auth.json();
      if (auth.ok) {
        // Set empty object so that it can make request to bakend and fetch user using accessToken
        setUser({});
        // redirect user to home page
        location.href = "/";
      } else {
        console.error(res);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async logoutUser() {
    try {
      const connection = await fetch(apiLogoutUser, {
        method: "POST",
        credentials: "include",
      });

      const response = await connection.json();
      if (connection.ok) {
        console.log("logged out");
        deleteUser();
        manageNavbar();
        // redirect user to home page
        location.href = "/";
      }
      if (connection.status === 401) {
        refreshToken();
      }
    } catch (e) {
      console.error(e);
    }
  }
}
