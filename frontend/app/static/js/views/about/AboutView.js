import AbstractView from "../AbstractView.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("About Us");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/about/templates/daisyUI/about.html",
      );
      const page = await html.text();
      this.page = page;
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div").innerHTML =
        "Error loading about";
    }
    const html = document.createElement("div");
    html.innerHTML = this.page;
    return html;
  }
}
