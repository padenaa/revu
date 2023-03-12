const callAPI = async (input) => {
    let data = {
        resume: input
    }
    const response = await fetch('http://localhost:8000/api/feedback', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    document.getElementById("input-area").classList.remove("is-loading")
    let resJSON = await response.json();
    feedback = resJSON['feedback'];
    console.log(feedback);
    document.getElementById("results").innerHTML = `
        <br><br><br><br>
        <h1 class="title-font"> Here's some feedback on your resume. Consider adding any suggestions that the rev-u AI makes:</h1>
        <br>
        <div class="card light-blue card-format">
            <div class"card-content card-format" style="margin-top: 10px;">
            <div class="content has-text-centered source-font">
                <p>✨${feedback}<p>
            </div>
            </div>
        </div>
        <img src="../robot.PNG" style="max-width:50%; height:auto;">
    `;
}
    

document.getElementById('button').addEventListener('click', () => {
    const input = document.getElementById('input').value;
    document.getElementById("input-area").classList.add("is-loading")
    callAPI(input);
});