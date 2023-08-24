# Todo
* Implement a function that assigns a court open to a specific Date:  DONE
* Fix the edit_activity because now it doesn't handle existing dates. DONE
* Format all the forms in the way edit_date.html does. DONE
* Do the validation for Activity and the three different types
    All of them need to have at least one court assigned
    'clinic'
        Has to be linked to an Event: DONE
    'private'
        Cannot to be linked to an Event: DONE
        Can have only one court assigned Court: DONE
    'court'
        Cannot to be linked to an Event: DONE 

* Override the dave method of the Date model in order to update the court everytime is saved.
    Do with @transaction.atomic: DONE

* In Date.get_courts() implement a way that the function takes as an argument if it's a clinic or not.

* Add different colors for each type of activity. If there is a pro assigned. Also, give a color to each pro.

* Create Test for models: 
    Member: Done
    Event: Done
    Activity: 
    Date
    Court
    Participation


