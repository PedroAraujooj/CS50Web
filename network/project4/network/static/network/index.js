const edit = (userId, postId) =>{
    postId = parseInt(postId);
    userId = parseInt(userId);
    fetch(`/edit/${postId}`)
        .then(response => response.json())
        .then(post => {
            if(post.user == userId){
                document.getElementById(post.id).innerHTML = `<form>
                <textarea name="text" rows="4" style="width: 100%" id ="edit-text"> ${post.text}</textarea>
                <br>
                <input type="submit" class="btn btn-primary" onclick="editPost(event, ${postId}, ${userId})" value="Edit">
                </form>`;
            }
            else{
                document.getElementById(post.id).innerHTML = "ERROR";
            }
        });

};
const editPost = (event, postId, userId) =>{
    event.preventDefault();
    let text = document.getElementById("edit-text").value;
    fetch(`/edit/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            text: text
        })
    }).then(response => response.json()).then(result => {
        console.log(result);
        document.getElementById(`${postId}`).innerHTML=`<h3>${text}</h3><p onclick="edit(${userId},${postId})" class="edit">Edit</p>`
    });
};

const like = (event, postId, likes) =>{
    event.preventDefault();
     fetch(`/like/${postId}`, {
         method: 'POST'
     }).then(response => response.json()).then(result => {
         console.log(result.message);
         console.log(document.getElementById(`like-${postId}`));
         if (result.message == "yes"){
             likes+=1;
             document.getElementById(`like-${postId}`).innerHTML=`<p><img src="/static/imgs/yes.png" alt="like" id = "like-${postId}-img" class="like" onclick="like(event,${postId}, ${likes})">${likes}</p>`;

         }
         else if(result.message == "no"){
             likes-=1;
             document.getElementById(`like-${postId}`).innerHTML=`<p><img src="/static/imgs/no.png" alt="like" id = "like-${postId}-img" class="like" onclick="like(event,${postId}, ${likes})">${likes}</p>`;

         }
         else{
              document.getElementById(`like-${postId}`).innerHTML="ERROR"
         }
     });
};