// Api endpoint
const baseUrl = "http://127.0.0.1:5000";
export const apiLoginUser = `${baseUrl}/api/v1/auth/login`;
export const apiSignupUser = `${baseUrl}/api/v1/auth/signup`;
export const apiLogoutUser = `${baseUrl}/api/v1/auth/logout`;
export const apiUploadPosts = `${baseUrl}/api/v1/posts/upload`;
export const apiUserInSession = `${baseUrl}/api/v1/user/auth`;
export const apiUser = `${baseUrl}/api/v1/user`;
export const apiProfileImage = `${baseUrl}/api/v1/getProfileImage`;
export const apiUserUpdateProfile = `${baseUrl}/api/v1/user/update`;
export const apiUserUpdateProfileImg = `${baseUrl}/api/v1/user/profileImg/update`;
export const apiUserPostsFeed = `${baseUrl}/api/v1/posts`;
export const apiHomeFeed = `${baseUrl}/api/v1/feed`;
export const apiAddFollower = `${baseUrl}/api/v1/user/follow`;
export const apiRemoveFollower = `${baseUrl}/api/v1/user/unfollow`;
export const apiTogglePostLike = `${baseUrl}/api/v1/posts/like`;
export const apiTogglePostBookmark = `${baseUrl}/api/v1/posts/bookmark`;
export const apiRefreshToken = `${baseUrl}/api/v1/auth/refresh`;
export const apiGetPostMedia = `${baseUrl}/api/v1/getPostMedia`;

export const apiComments = `${baseUrl}/api/v1/comments`;
export const apiCreateComment = `${baseUrl}/api/v1/comments/create`;
export const apiUpdateComments = `${baseUrl}/api/v1/comments/update`;
export const apiDeleteComment = `${baseUrl}/api/v1/comments/delete`;

// Global user object
export function setUser(sessionUser) {
  localStorage.setItem("payload", JSON.stringify(sessionUser));
}

export function getUser() {
  let _user = localStorage.getItem("payload");
  return _user ? JSON.parse(_user) : null;
}

export function deleteUser() {
  localStorage.removeItem("payload");
}

// Store macro components in memory
let postMacroTemplate = {};

export async function initializeTemplate({ feedMacro = true }) {
  let templateHtml;
  const feedPostMacro =
    "/static/daisyUI/macroComponent/feedPostLayoutMacro.html";
  const userPostMacro =
    "/static/daisyUI/macroComponent/userPostLayoutMacro.html";
  try {
    if (postMacroTemplate[feedMacro ? feedPostMacro : userPostMacro]) {
      templateHtml =
        postMacroTemplate[feedMacro ? feedPostMacro : userPostMacro];
    } else {
      const res = await fetch(feedMacro ? feedPostMacro : userPostMacro);
      templateHtml = await res.text();

      // Add template to memory
      postMacroTemplate[feedMacro ? feedPostMacro : userPostMacro] =
        templateHtml;
    }

    const tempContainer = document.createElement("div");
    tempContainer.innerHTML = templateHtml;

    document.body.appendChild(tempContainer);

    const postTemplate = document.getElementById("postCardMacro");
    return postTemplate; // resolve when fully loaded
  } catch (error) {
    console.error(error);
  }
}

export async function fetchUserInfo() {
  if (!getUser()) {
    return;
  }
  try {
    const res = await fetch(apiUserInSession, {
      method: "GET",
      credentials: "include",
    });
    const resObj = await res.json();
    if (res.ok) {
      setUser(resObj.payload);
      manageNavbar();
    } else if (res.status === 401) {
      await refreshToken();
    }
  } catch (error) {
    console.error(error);
  }
}

export async function refreshToken() {
  try {
    const response = await fetch(apiRefreshToken, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "GET",
      credentials: "include",
    });

    if (response.ok) {
      await fetchUserInfo();
    } else {
      flash("Session expired. Please log in again.", { messageType: "error" });
      deleteUser();
      manageNavbar();
    }

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Navbar
export function manageNavbar() {
  const profileBtnContainer = document.getElementById("profileBtnContainer");
  const signupLoginContainer = document.getElementById("signupLoginContainer");
  const user = getUser();
  console.log(user);
  if (user) {
    profileBtnContainer.classList.remove("hidden");
    const ankerTag = profileBtnContainer.querySelector("#goToProfile");
    ankerTag.href = `/user/${user.userName}`;
    const loggedProfileLogo =
      profileBtnContainer.querySelector("#loggedProfileLogo");
    loggedProfileLogo.src = user.profileImgUrl;
    signupLoginContainer.classList.add("hidden");
  }
}

export async function loadSessionUser() {
  if (!getUser()) {
    await fetchUserInfo();
  }
}

export function flash(message, { duration = 3000, messageType = "success" }) {
  let bgColor;
  switch (messageType) {
    case "success":
      bgColor = "#4caf50";
      break;
    case "error":
      bgColor = "#f44336";
      break;
    case "warning":
      bgColor = "#ffc107";
      break;
    case "info":
      bgColor = "#2196f3";
      break;
    default:
      bgColor = "#212121";
      break;
  }

  const toast = document.querySelector(".toast");
  toast.textContent = message;
  toast.style.backgroundColor = bgColor;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, duration);
}
