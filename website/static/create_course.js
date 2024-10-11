window.onload(fetchCourse())

function fetchCourse() {
    const course_id = document.getElementById('overall-course-container').getAttribute('data-course-id');

    fetch('/fetch4js', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ course_id: course_id })  
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.error) {
            console.error('Course not found');
        } else {
            let titleInp = document.getElementById("course-title");
            let shortDesc = document.getElementById("short-course-desc");
            let fullDesc = document.getElementById("full-course-desc");
            let courseType = document.getElementById("course_type");
            let skillLevel = document.getElementById("skill_level");

            if (data.title.length !== 50) {
                titleInp.value = data.title;
            }

            if (data.shortDesc.length !== 50) {
                shortDesc.value = data.short_desc;
            }

            if (data.fullDesc.length !== 50) {
                fullDesc.value = data.full_desc
            }

            courseType.value = data.type
            skillLevel.value = data.level
        }
    })
    .catch(error => console.error('Error fetching course:', error));
}

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

