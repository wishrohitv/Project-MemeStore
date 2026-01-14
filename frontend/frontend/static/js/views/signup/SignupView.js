import AbstractView from "../AbstractView.js";

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
      this.page = page;
    } catch (error) {
      console.error(error);
      this.page = "Error loading signup page";
    }
    const html = document.createElement("div");
    html.innerHTML = this.page;
    return html;
  }
}
