# Todo
* I need to fix the DateManager: The can create manager doesn't take into account the courts
that are already been used. It needs to find open courts. If not, then and only then throw an
error.
* Implement a function that assigns a court open to a specific Date:  DONE
* Fix the edit_activity because now it doesn't handle existing dates.
* Format all the forms in the way edit_date.html does.
* Do the validation for Activity and the three different types
    All of them need to have at least one court assigned
    'clinic'
        Has to be linked to an Event
    'private'
        Cannot to be linked to an Event
        Can have only one court assigned Court
    'court'
        Cannot to be linked to an Event
* Create Test for models: 
    Member
    Event
    Activity
    Date
    Court
    Participation


