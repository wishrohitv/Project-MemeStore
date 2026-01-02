
let name = document.getElementById("uName")
let userName = document.getElementById("userName")
let bio = document.getElementById("bio")

// imgUploadButton
let imgUploadButtonBox = document.getElementById("imgUploadButton")
// Currently selected profile image by user
let selectedInputFile = document.getElementById('selectedProfileImg')

// function to fetch user's profile data
async function fetchUserProfileData() {
    try {
        let connection = await fetch(
            apiUserProfile,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json; charset=utf-8"
                },
                body: JSON.stringify({ "uid": loggedUserUid })
            }
        )
        let res = await connection.json()

        console.log(res.payload)
        name.value = res.payload["name"]
        userName.value = res.payload["userName"]
        fetchProfileImg(userName.value, previewBox)
    } catch (e) {
        console.error(e)
    }
}

fetchUserProfileData()

let previewBox = document.getElementById("profilePreview")
var loadFile = function (event) {
    var reader = new FileReader();
    reader.onload = function () {
        let fileName = event.target.files[0].type
        //    if(fileName==="image/png"){
        //      previewBox.src = reader.result;
        //    }else {
        //        console.error("Unsupported file type")
        //    }
        // show img upload button
        imgUploadButtonBox.classList.remove("hidden")
        previewBox.src = reader.result
    };
    reader.readAsDataURL(event.target.files[0]);
};

async function imgUploadButton() {
    let data = new FormData()
    console.log(selectedInputFile.files[0])
    for (const file of selectedInputFile.files) {
        data.append('files', file, file.name)
        data.append("userName", userName.value)
    }
    console.log(data)
    let res = await fetch(apiUpdateProfile, {
        method: "POST",
        credentials: "include",
        body: data
    }
    )
    let re = await res.json()
    console.log(res.ok)
    console.log(re)
}
