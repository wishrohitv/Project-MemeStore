async function togglePostLike(postID, event) {
  try {
    let res = await fetch(`${apiTogglePostLike}/${postID}`, {
      method: "PUT",
      credentials: "include",
    });
    // console.log(event);
    // console.log(event.target.parentNode);
    // console.log(event.target.parentNode.parentNode);
    let re = await res.json();
    if (res.ok) {
      changeLikeSvgs(res.isLiked, event.target.parentNode.parentNode);
    }
    console.log(re);
  } catch (e) {
    console.error(e);
  }
}

function changeLikeSvgs(isLiked, svgContainer) {
  if (isLiked) {
    svgContainer.children[1].classList.remove("hidden");
    svgContainer.children[0].classList.add("hidden");
  } else {
    svgContainer.children[1].classList.add("hidden");
    svgContainer.children[0].classList.remove("hidden");
  }
  Window.backgroundColor = "red";
  console.log(svgContainer.children[0].classList);
  console.log(svgContainer.children[1].classList);
}
