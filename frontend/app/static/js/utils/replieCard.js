import { apiUploadPosts } from "./base.js";
import { createMediaPreview } from "./replieMediaPreview.js";

export async function replieCard(postID) {
  try {
    const html = await fetch("/static/daisyUI/macroComponent/replieMacro.html");
    const replieHtml = await html.text();
    const replieMarco = document.createElement("div");
    replieMarco.innerHTML = replieHtml;
    const form = replieMarco.querySelector("form");
    const imgPreview = replieMarco.querySelector("#imgPreview");
    const selectedFile = replieMarco.querySelector("#selectedFile");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      console.log(formData);
      try {
        const connection = await fetch(
          apiUploadPosts + `?parentPostID=${postID}&isReplie=True`,
          {
            method: "POST",
            credentials: "include",
            body: formData,
          },
        );
        console.log(connection.status);
        console.log(await connection.json());
      } catch (e) {
        console.error(e);
      }
    });

    // Listen button click event and fire file picker
    replieMarco
      .querySelector("#filePickerBtn")
      .addEventListener("click", (e) => {
        selectedFile.click();
      });
    // Listen file change event and preview image
    selectedFile.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (file) {
        imgPreview.classList.remove("hidden");
        if (imgPreview.children.length > 0) {
          imgPreview.removeChild(imgPreview.firstChild);
        }
        imgPreview.appendChild(await createMediaPreview(file));
      }
    });
    return replieMarco;
  } catch (error) {
    console.error(error);
    return null;
  }
}
