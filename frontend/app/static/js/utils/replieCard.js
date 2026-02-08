import { apiUploadPosts } from "./base.js";

export async function replieCard(postID) {
  try {
    const html = await fetch("/static/daisyUI/macroComponent/replieMacro.html");
    const replieHtml = await html.text();
    const replieMarco = document.createElement("div");
    replieMarco.innerHTML = replieHtml;
    const form = replieMarco.querySelector("form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(form);

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
    });
    const imgPreview = replieMarco.querySelector("#imgPreview");
    replieMarco
      .querySelector("#filePickerBtn")
      .addEventListener("click", (e) => {
        const filePicker = showOpenFilePicker();
        console.log(filePicker);
        filePicker
          .then((file) => {
            console.log(file);
            imgPreview.src = file.name;
            imgPreview.classList.remove("hidden");
          })
          .catch((error) => console.log(error));
      });
    return replieMarco;
  } catch (error) {
    console.error(error);
    return null;
  }
}
