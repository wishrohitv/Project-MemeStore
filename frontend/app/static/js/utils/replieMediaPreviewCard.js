export async function createMediaPreview(file, onRemoveClbk) {
  try {
    const html = await fetch(
      "/static/daisyUI/macroComponent/replieMediaPreviewMacro.html",
    );
    const previewMacro = await html.text();

    const preview = document.createElement("div");
    preview.innerHTML = previewMacro;
    const img = preview.querySelector("#imgPreview");
    const video = preview.querySelector("#videoPreview");
    if (file.type.startsWith("image/")) {
      img.classList.remove("hidden");
      video.classList.add("hidden");
      img.src = URL.createObjectURL(file);
    } else if (file.type.startsWith("video/")) {
      video.classList.remove("hidden");
      img.classList.add("hidden");
      video.src = URL.createObjectURL(file);
    }
    const removeBtn = preview.querySelector("#removeBtn");
    removeBtn.addEventListener("click", () => {
      URL.revokeObjectURL(img.src || video.src); // Avoid memory leaks
      onRemoveClbk();
      preview.remove();
    });
    return preview;
  } catch (e) {
    console.error(e);
  }
}
