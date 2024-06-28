$(document).ready(function() {

    // validation for user registration form
    $(".registeruser").children("#registerform").submit(function (e) {
        e.preventDefault();
        $(".errormsg").remove();

        var isValid = true;

        $(this).find('input[type="text"],input[type="password"],input[type="email"]').each(function () {
            var fieldval = $(this).val();
            var err = $('<div class="errormsg">Field is empty!</div>');
            var emailerr = $('<div class="errormsg">Enter a valid VT email address!</div>');
            if (fieldval === "") {
                $(this).css("border", "2px solid red");
                err.insertAfter($(this));
                isValid = false; // Set isValid to false if any field is empty
            } else if ($(this).is('#register-email')) {
                if (!fieldval.endsWith("vt.edu")) {
                    // checking if email is a valid vt address or else throw an error
                    $(this).css("border", "2px solid red");
                    emailerr.insertAfter($(this));
                    isValid = false; // Set isValid to false if any field is empty
                }


            } else {
                $(this).css("border", "none");
            }
        });


        if (isValid) {
            // If all fields are valid, submit the form
            $(this).unbind('submit').submit();
        }

    });


     // validation for user editing profile form
//     $(".profile").children("#savechanges").submit(function (e) {
//         e.preventDefault();
//         $(".errormsg").remove();
//
//         var isValid = true;
//
//
//             var fieldval = $('#checkemail').val();
//             console.log(fieldval);
//
//             var emailerr = $('<div class="errormsg">Enter a valid VT email address!</div>');
//
//                 if (!fieldval.endsWith("vt.edu")) {
//                     // checking if email is a valid vt address or else throw an error
//                     $('#checkemail').css("border", "2px solid red");
//                     emailerr.insertAfter($('#checkemail'));
//                     isValid = false; // Set isValid to false if any field is empty
//                 }
//
//
//              else {
//                 $('#checkemail').css("border", "none");
//             }
//
//
//         if (isValid) {
//             // If all fields are valid, submit the form
//             $(this).unbind('submit').submit();
//         }
//
//     });
//
//
});