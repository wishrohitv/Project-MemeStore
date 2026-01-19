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
    await fetch(apiSignupUser, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        history.pushState({}, "", "/login");
      } else {
        console.error("Signup failed");
      }
    });
  } catch {
    console.error("Signup failed");
  }
}
