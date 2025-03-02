const button = document.getElementById("Fit-Me-Button");

button.innerText = "Fit Me";
Object.assign(button.style, {
    fontSize: '1rem',
    padding: '12px 28px',
    textAlign: 'center',
    marginBottom: '15px',
    borderRadius: '4px',
    borderColor: 'black',
    backgroundColor: 'white',
    transitionDuration: '0.4s',
    font: "bold"
});


button.addEventListener('click', runPipeline);

function runPipeline(){
    console.log("Hi");
    
}