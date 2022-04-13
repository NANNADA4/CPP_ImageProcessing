const card = document.querySelector(".card");
const EntryImage = document.querySelector(".EntryImage img");
const title = document.querySelector(".title");
const subtitle = document.querySelector(".subtitle");
const LinkTo = document.querySelector(".LinkTo");

card.addEventListener("mousemove", function (e) {
    let xAxis = (window.innerWidth / 2 - e.pageX) / 60;
    let yAxis = (window.innerHeight / 2 - e.pageY) / -30;
    card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
});

card.addEventListener("mouseenter", function (e) {
    card.style.transition = "none";
    title.style.transform = "translateZ(100px)";
    subtitle.style.transform = "translateZ(70px)";
    LinkTo.style.transform = "translateZ(50px)";
});

card.addEventListener("mouseleave", function (e) {
    card.style.transition = "all 0.5s ease";
    card.style.transform = "rotateX(0deg) rotateY(0deg)";
    title.style.transform = "translateZ(0px)";
    subtitle.style.transform = "translateZ(0px)";
    LinkTo.style.transform = "translateZ(0px)";
});

card.addEventListener("mouseenter", (e) => {
    EntryImage.style.transform = "rotateZ(-45deg) translateZ(150px)";
});

card.addEventListener("mouseleave", (e) => {
    EntryImage.style.transform = "rotateZ(0deg) translateZ(0px)";
});

function ClickTitle(t) {
    subtitle.innerHTML = t;
}
