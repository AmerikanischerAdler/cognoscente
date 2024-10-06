function addLesson() {
    const addBtn = document.querySelector(".addBtn");
    const plus = document.getElementById("plusIcon");
    const minus = document.getElementById("minusIcon");
    const revealBtn = document.getElementById("revealBtn");

    if (addBtn.classList.contains("hidden")) {
        addBtn.classList.remove("hidden");
        addBtn.style.display = "flex";
        addBtn.style.alignItems = "center";
        addBtn.style.justifyContent = "center";
        addBtn.style.marginLeft = "4%";

        plus.style.display = "none";
        minus.style.display = "inline";

        revealBtn.classList.remove("hidden"); 
    } else {
        addBtn.classList.add("hidden");
        addBtn.style.display = "none";
        plus.style.display = "inline";
        minus.style.display = "none";
        revealBtn.classList.add("hidden"); 
    }
}

function toggleContent() {
    const revealContent = document.getElementById("revealContent");
    const plus = document.getElementById("plusIcon2");
    const minus = document.getElementById("minusIcon2");

    if (revealContent.classList.contains("hidden")) {
        revealContent.classList.remove("hidden");

        revealContent.style.display = "flex";
        revealContent.style.alignItems = "center";
        revealContent.style.justifyContent = "space-evenly";

        plus.style.display = "none";
        minus.style.display = "inline";
    } else {
        revealContent.classList.add("hidden");
        revealContent.style.display = "none";
        plus.style.display = "inline";
        minus.style.display = "none";
    }
}

