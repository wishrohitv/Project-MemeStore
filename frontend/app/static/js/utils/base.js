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

export async function initializeTemplate() {
  try {
    const res = await fetch(
      "/static/daisyUI/macroComponent/postLayoutMacro.html",
    );
    const templateHtml = await res.text();
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
