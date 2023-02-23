document.addEventListener('DOMContentLoaded', function () {
    var listView = document.querySelector('.list-view');
    var gridView = document.querySelector('.grid-view');
    var newProject = document.querySelector('.add-btn');
    var projectsList = document.querySelector('.project-boxes');
    
    listView.addEventListener('click', function () {
      gridView.classList.remove('active');
      listView.classList.add('active');
      projectsList.classList.remove('jsGridView');
      projectsList.classList.add('jsListView');
    });
    
    gridView.addEventListener('click', function () {
      gridView.classList.add('active');
      listView.classList.remove('active');
      projectsList.classList.remove('jsListView');
      projectsList.classList.add('jsGridView');
    });


    newProject.addEventListener('click', function () {
      const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-success'
        },
        buttonsStyling: false
      })
      
      swalWithBootstrapButtons.fire({
        title: 'What would you like to create?',
        text: "If you want to create a new event from scratch, you should start with event.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Event',
        cancelButtonText: 'Clinic',
      }).then((result) => {
        if (result.isConfirmed) {
          location.href="/create_event"
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          location.href="/create_clinic"
        }
      })
    });
  });