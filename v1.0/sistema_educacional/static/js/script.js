const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i=> {
            i.parentElement.classList.remove('active');

        })
        li.classList.add('active');
    

    });
});

// TOGGLE SIDEBAR

const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function (e) {
    // Verifica se o clique ocorreu no ícone do menu
    if (e.target.classList.contains('bx-menu') || e.target.parentElement.classList.contains('bx-menu')) {
        sidebar.classList.toggle('hide');
    }
});



const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
    if(window.innerWidth < 576 ) {
        e.preventDefault();
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchButtonIcon.classList.replace('bx-search', 'bx-x');
        }else{
            searchButtonIcon.classList.replace('bx-x', 'bx-search');

        }

    }
})


if(window.innerWidth < 768) {
    sidebar.classList.add('hide');
    alert("Eu sou um\nAlert!");
}else if (window.innerWidth > 576){
    searchButtonIcon.classList.replace('bx-x', 'bx-search');
    searchForm.classList.remove('show');

}

window.addEventListener('resize', function() {
    if (this.innerWidth > 576){
        searchButtonIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
})

