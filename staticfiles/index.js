function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
let languages = document.getElementById("languages");
let frequency = document.getElementById("frequency");
let autosave = document.getElementById("autosave");
languages.addEventListener("change", () => {
    setCookie("languages", languages.value, 365);
});
frequency.addEventListener("change", () => {
    setCookie("frequency", frequency.value, 365);
});
autosave.addEventListener("change", () => {
    setCookie("autosave", autosave.checked, 365);
});
if (getCookie("languages")) {
    languages.value = getCookie("languages");
} else {
    setCookie("languages", "Spanish", 365);
}
if (getCookie("frequency")) {
    frequency.value = getCookie("frequency");
} else {
    setCookie("frequency", "15", 365);
}
if (getCookie("autosave")) {
    autosave.checked = getCookie("autosave") === "true";
} else {
    setCookie("autosave", "true", 365);
}
const increment = () => {
  if (Number(frequency.value) + 5 < 100) {
    frequency.value = Number(frequency.value) + 5;
    setCookie("frequency", frequency.value, 365);
  }
}
const decrement = () => {
  if (Number(frequency.value) - 5 >= 10) {
    frequency.value = Number(frequency.value) - 5;
    setCookie("frequency", frequency.value, 365);
  }
}
document.querySelector('.spinner.increment').addEventListener('click', increment);
document.querySelector('.spinner.decrement').addEventListener('click', decrement);
let lastFiveList = JSON.parse(localStorage.getItem('autosave_list'));
if (lastFiveList) {
    lastFiveList = lastFiveList.slice(-5).reverse();
    lastFiveList.forEach(item => {
        const div = document.createElement('div');
        div.innerHTML = `<strong>${item.word}</strong><br/>${item.translation}<br/><small>Language: ${item.language}</small>`;
        div.className = 'notice width-sm';
        div.setAttribute("onclick", "searchGoogle(`" + item.translation + "`, `" + item.language + "`)");
        document.querySelector('.words-min-grid').appendChild(div);
    });
    const listDiv = document.createElement('div');
    listDiv.innerHTML = `<i><strong>Check out your full list <span class='accented' style='cursor:pointer' onclick="window.location.href='/list/'">here</span></strong></i>`;
    listDiv.style.marginTop = '-25px';
    listDiv.style.marginBottom = '-5px';
    document.querySelector('.words-min-grid').appendChild(listDiv);
} else {
    const div = document.createElement('p');
    div.innerHTML = `<p>Well this is awkward... looks like you have no words yet. Go read some articles!</p>`;
    div.style.marginTop = '-25px';
    div.style.marginBottom = '-10px';
    document.querySelector('.words-min-grid').appendChild(div);
}
function searchGoogle(searchTerm, lang) {
    const url = `https://www.google.com/search?q=${encodeURIComponent(searchTerm)}+meaning+in+${lang}`;
    window.open(url, '_blank');
}