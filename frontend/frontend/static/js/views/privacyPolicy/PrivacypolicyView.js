import AbstractView from "../AbstractView.js";

export default class extends AbstractView {
  constructor(params) {
    super(params);
    this.setTitle("Privacy and Policy");
  }

  async getHtml() {
    try {
      const html = await fetch(
        "/static/js/views/privacyPolicy/templates/daisyUI/privacyPolicy.html",
      );
      const page = await html.text();
      this.page = page;
    } catch (error) {
      console.error(error);
      this.page = document.createElement("div").innerHTML =
        "Error loading privacyPolicy";
    }
    const html = document.createElement("div");
    html.innerHTML = this.page;
    return html;
  }
}
