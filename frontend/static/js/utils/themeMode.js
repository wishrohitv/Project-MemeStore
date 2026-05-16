//let systemTheme window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
let initialTheme = localStorage.getItem("mode")

let ldm = document.getElementsByClassName("light-dark-button")

let themeMode = document.documentElement
if (initialTheme == null) {
  localStorage.setItem("mode", "light")
  themeMode.dataset.theme = "light"
} else {
  themeMode.dataset.theme = initialTheme
}
function setLDM() {
  let mode = localStorage.getItem("mode")
  if (mode === "light") {
    localStorage.setItem("mode", "dark")
    themeMode.dataset.theme = "dark"

    ldm[0].children[0].classList.add("hidden")
    ldm[0].children[1].classList.remove("hidden")
  } else if (mode === "dark") {
    themeMode.dataset.theme = "light"
    localStorage.setItem("mode", "light")
    ldm[0].children[1].classList.add("hidden")
    ldm[0].children[0].classList.remove("hidden")
  }
}