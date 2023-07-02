/*=============== LINK ACTIVE ===============*/
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    linkColor.forEach(l => l.classList.remove('active-link'))
    this.classList.add('active-link')
}


function filterParticipants() {
  const parentDiv = document.getElementById('id_participants');
  const childDivs = parentDiv.getElementsByTagName('div');

  const input = document.getElementById('filterInput');
  input.addEventListener('input', () => {
    const filterValue = input.value.toLowerCase();
    for (let i = 0; i < childDivs.length; i++) {
      const childDiv = childDivs[i];
      const textContent = childDiv.textContent.toLowerCase();
      if (textContent.includes(filterValue)) {
        childDiv.style.display = 'block';
      } else {
        childDiv.style.display = 'none';
      }
    }
  });
}

linkColor.forEach(l => l.addEventListener('click', colorLink))

/*=============== SHOW HIDDEN MENU ===============*/
const showMenu = (toggleId, navbarId) =>{
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId)

    if(toggle && navbar){
        toggle.addEventListener('click', ()=>{
            /* Show menu */
            navbar.classList.toggle('show-menu')
            /* Rotate toggle icon */
            toggle.classList.toggle('rotate-icon')
        })
    }
}
showMenu('nav-toggle','nav')