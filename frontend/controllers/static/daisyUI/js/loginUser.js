let email = document.getElementById("email")
let password = document.getElementById("password")

async function authUser() {
    console.log(email.value)
    console.log(password.value)
    let auth = await fetch(apiAuthenticateUser, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(
            {
                "email": email.value,
                "password": password.value
            }
        )
    }
    )
    let res = await auth.json()
    if (auth.ok) {
        console.log("logged in")
        addUserInSession(res["userID"], res["userName"])
    }

}

async function addUserInSession(id, userName) {
    let user = await fetch(`/userSession/setUser/${id}/${userName}`)
    let res = await user.json()
    if (user.ok) {
        localStorage.setItem("uid", id)
        localStorage.setItem("userName", userName)

        // redirect user to home page
        location.href = "/";
    }
    else {
        console.error(res)
    }
}

async function removeUser(id = null, userName = null) {
    console.log("remove called")
    let user = await fetch(`/userSession/removeUser?id=${id}&userName=${userName}`)
    let res = await user.json()
    if (user.ok) {
        // redirect user to home page
        console.log(res);
        localStorage.clear();
        location.href = "/";
    }
    else {
        console.error(res)
    }
}