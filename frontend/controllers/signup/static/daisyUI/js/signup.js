const form = document.querySelector("#signupForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault(); // Stop the page from reloading

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries()); // Convert form to simple object
  console.log(data);
  signup(data);
});

async function signup(data) {
  try {
    fetch(apiSignupUser, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  } catch {
    console.error("Signup failed");
  }
}
