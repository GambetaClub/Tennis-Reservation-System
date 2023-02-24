function getCheckedDates(){
    // Returns a list with the ids of the dates selected
    var checkedDates = []; 
    var inputElements = document.getElementsByClassName('checkbox-input');
    for(var i=0; inputElements[i]; ++i){
        if(inputElements[i].checked){
            checkedDates.push(inputElements[i].value);
        }
    }
    return checkedDates;
};


$(document).on('submit', '#dates-form', function(e){
    e.preventDefault();
    var endpoint = $("#dates-form").attr("data-url");
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    dates = JSON.stringify(getCheckedDates());
    event_id = document.querySelector('#event_id').value;
    $.ajax({
        type : "POST",
        url: endpoint,
        dataType: "json",
        data: {
            'dates': dates,
            'event_id': event_id
        },
        headers: {'X-CSRFToken': csrf_token},
        success: function(response){
            Swal.fire({
                title: 'Success',
                text: response.message,
                icon: 'success',
                confirmButtonText: 'Thank you!',
              }).then((result) => {
                window.location.href = document.referrer;
            })
            return false;

        },
        error: function(response){
            Swal.fire({
                title: 'Careful',
                text: response.responseJSON.message,
                icon: 'warning',
                confirmButtonText: 'Ok',
              })
        }
    })
});


