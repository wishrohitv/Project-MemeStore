import { apiUploadPosts } from "../utils/base.js";
import { createMediaPreview } from "./replieMediaPreviewCard.js";

export async function replieCard(postID) {
  try {
    const html = await fetch("/static/daisyUI/macroComponent/replieMacro.html");
    const replieHtml = await html.text();
    const replieMarco = document.createElement("div");
    replieMarco.innerHTML = replieHtml;
    const form = replieMarco.querySelector("form");
    const previewContainer = replieMarco.querySelector("#previewContainer");
    const selectedFile = replieMarco.querySelector("#selectedFile");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
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
        previewContainer.classList.remove("hidden");
        if (previewContainer.children.length > 0) {
          previewContainer.removeChild(previewContainer.firstChild);
        }
        previewContainer.appendChild(
          await createMediaPreview(file, (onRemove) => {
            selectedFile.value = ""; // This resets the selected file
          }),
        );
      }
    });
    return replieMarco;
  } catch (error) {
    console.error(error);
    return null;
  }
}
