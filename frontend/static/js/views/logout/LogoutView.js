import AbstractView from "../AbstractView.js";
import { apiLogoutUser, deleteUser, manageNavbar } from "../../utils/base.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Login");
  }

  async getHtml() {
    try {
      this.page = document.createElement("div");

      this.page.innerHTML = "Logout in progress";
      this.logoutUser();
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div");
      this.page.innerHTML = "Error logout page";
    }

    return this.page;
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
