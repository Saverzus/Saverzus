

// 1 Свайп на стринце с регистрацией и логином
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});



//2 header>nav> class=active
var menu = document.querySelectorAll('.nav_menu_activator li a');
    for (var j = menu.length - 1; j >= 0; j--) {
        if (menu[j].href==document.URL) {
            menu[j].setAttribute("class", "active"+j);
            console.log(j)      
        }
    };

// 3 Цикл для присвоения ACTIVE к элементам меню ПРОФИЛЯ (Стена, Друзья, Фото)
var profile_menu = document.querySelectorAll('.profile_menu li a');
    for (var i = profile_menu.length - 1; i >= 0; i--) {
        if (profile_menu[i].href==document.URL) {
            profile_menu[i].setAttribute("class", "active");
        }
    };
// 4 lenta>category>ul>li
var lenta = document.querySelectorAll('.lenta_nav li a');
    for (var k = lenta.length - 1; k >= 0; k--) {
        if (lenta[k].href==document.URL) {
            lenta[k].setAttribute("class", "active");
            //console.log(k)      
        }
    };



