

    // user interaction 1 (DOM traversal) for the sell page form.
        // Modifying existing element- If the input (type=text)& textarea fields are empty, then the field's border will
    //  turn red indicating error condition.
        // Adding new element- An error message saying "Field is empty"
    // is added below the text input area.


$(document).ready(function() {

     $(".sellitem").children("#sellform").submit(function(e) {
        e.preventDefault();
        $(".errormsg").remove();

        var isValid = true;

        $(this).find('input[type="text"],textarea').each(function() {
            var fieldval = $(this).val();
            var err = $('<div class="errormsg">Field is empty!</div>');
            var noerr = $('<div class="errormsg">Enter a valid number!</div>');
            if($(this).is('#price'))
            {
                if(isNaN(fieldval))
                {
                     $(this).css("border", "2px solid red");
                    noerr.insertAfter($(this));
                    isValid = false; // Set isValid to false if any field is empty
                }
                else if (fieldval=="")
                {
                    $(this).css("border", "2px solid red");
                    err.insertAfter($(this));
                    isValid = false; // Set isValid to false if any field is empty
                }
            }
            else {
                if (fieldval === "") {
                    $(this).css("border", "2px solid red");
                    err.insertAfter($(this));
                    isValid = false; // Set isValid to false if any field is empty
                } else {
                    $(this).css("border", "none");
                }
            }
        });

        if (isValid) {
            // If all fields are valid, submit the form
            $(this).unbind('submit').submit();
        }

    });






 //
 // user interaction 2 (event delegation) for category navbar on furniture.html page( page listing items).
 //        Modifying existing element- Underlining the selected navigation.
 //        Adding new element- A message regarding the results.

    $(".itemcategories").on("click", ".categories", function(event) {
        // event.preventDefault();
        $(".categories").removeClass("underline");
        $(this).addClass("underline").css("text-decoration-color", "var(--primary-color3)");

    });


         // 1st ajax interaction . function for dynamically showing subcategories from selected category by the user using ajax request

         $("input[type='radio'][data-category]").on("change", function(){
            // checking if category radio button has been selected and if so sending it to get its respective subcategories
           if ($(this).is(":checked")) {
               // access the selected category and send it to fetch the subcategories
           var selectedcategory = $(this).attr('data-category');
           var ajax_url = $(this).attr('data-ajax-url');
           getsubcategories(selectedcategory, ajax_url);
         }

         });


         // function to get subcategories using ajax request
        function getsubcategories(selectedcategory,ajax_url)
        {
            // sending ajax request to fetch the list of subcategories
                   $.ajax({

                  // The URL for the request
                   url: ajax_url,

                  // The data to send (will be converted to a query string)
                      data: {
                       category:selectedcategory
                       },

                  // Whether this is a POST or GET request
                     type: "GET",

                    // The type of data we expect back
                     dataType : "json",

                   })

                       // finding and replacing the subcategories labels and changing the value of respective input fields
                .done(function(json) {
                    var optionDivs = $('#subcategories').find('.option');
                     json.subcategories.forEach(function(subcategory,index){
                     var currentOptionDiv = optionDivs.eq(index);
                     currentOptionDiv.find('input[type="radio"]').attr('value',subcategory);
                     currentOptionDiv.find('label').text(subcategory);
                     })

                })
                // Code to run if the request fails; the raw request and
                       // status codes are passed to the function
                .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
                })
                 // Code to run regardless of success or failure;
                // .always(function( xhr, status ) {
                //  alert( "The request is complete!" );
                // });
            }


  // 2nd ajax interaction - comment box and displaying comments on UI

         $(".commentsection").on("click", "#comment", function(event) {

             event.preventDefault();
               // accessing the comment added by the user
                var commenturl=$(this).data('comment-url');
                var comment=$("#commentbox").val();
                addcomment(commenturl,comment);
           });


        // function to add the comment and display on the UI using AJAX
        function addcomment(commenturl,comment) {
            // sending ajax request with comment to be added as data
            $.ajax({
                url: commenturl,
                data: {
                    comment:comment,
                },
                type: "POST",
                dataType: "json",
                headers: {'X-CSRFToken': csrftoken}

            })

            .done(function(json) {

                // appending the new comment to the already existing comments and display . Every comment displays the name of the author, date of the comment and the comment
            if(json.success)
            {   var newCommentBox = $('<div class="individualcommentbox newbox">');
                var date = new Date(json.date);
                var formattedDate = date.toLocaleString();
                  newCommentBox.append('<p id="commentauthor"> @ <a href="{% url "users:profile_detail" "' + json.author + '" %}">' + json.author + '</a>  •  ' + formattedDate + '</p>');

                     newCommentBox.append('<p id="commentbyauthor">' + json.message + '</p>');
                      newCommentBox.append('<div class="commentbuttonbox">' +
                          '<button class="commentbuttons edit-comment" id="editcommentbutton" data-editcomment-id="' + json.id + '">Edit</button>' +
                     '<button class="commentbuttons delete-comment" id="deletecomment" data-deletecomment-url="/studentswap/deletecomment/'+ json.id +'/" data-comment-id="' + json.id + '">Delete</button>' +
                     '</div>');

                        // Append the comment button box to the new comment

                     $('.pastcomments').prepend(newCommentBox);
                      $('#commentbox').val("");

                      // editing and updating  new comment
                newCommentBox.on('click', '.edit-comment', function(event) {

                 event.preventDefault();
                 var commentId = $(this).data("editcomment-id");
                 $(".editcomment").hide();
                 $(".commentbuttonbox").hide();
                 $("#commentbyauthor").hide();
               // Create a new edit form
                      newCommentBox.append('<form class="editcomment" id="editcomment-' + commentId + '" >\n' +
                 '    <input type="text" value="" id="editcommentbox-' + commentId + '">\n' +
                          ' <button class="commentbuttons savecomment" data-savecomment-url="/studentswap/savecomment/' + commentId + '/" data-savecomment-id="' + commentId + '">Save changes</button>\n' +
                  '</form>');

                 
            });

                //saving the new comment
              newCommentBox.on("click", ".savecomment", function (event) {
                event.preventDefault();

                 // Accessing the comment edited by the user
                 var commentId = $(this).data("savecomment-id");
                 var comment = $("#editcommentbox-" + commentId).val();
                  var commenturl = $(this).data("savecomment-url");

                 // Update comment using AJAX
                updatecomment(commenturl, comment, commentId);
            });


             // deleting new comment
            newCommentBox.on('click', '.delete-comment', function(event) {
            event.preventDefault();
            // accessing the comment added by the user
            var commentId = $(this).data('comment-id');
            var commenturl = $(this).data('deletecomment-url');
            deletecomment(commenturl, commentId);
        });

                 }


                })
                .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
                })

        }



        // ajax interaction for deleting comment

            $(".commentbuttonbox").on("click",".delete-comment", function(event) {

             event.preventDefault();
               // accessing the comment added by the user
                var commentId = $(this).data('comment-id');
                var commenturl=$(this).data('deletecomment-url');
                deletecomment(commenturl,commentId);
           });
         function deletecomment(commenturl,commentId) {
            // sending ajax request with comment to be added as data
            $.ajax({
                url: commenturl,
                data: {
                       commentId: commentId
                },
                type: "POST",
                dataType: "json",
                headers: {'X-CSRFToken': csrftoken}

            })

            .done(function(json) {

                // appending the new comment to the already existing comments and display . Every comment displays the name of the author, date of the comment and the comment
                 if(json.success)
                 {  alert("Comment deleted successfully");
                     // remove comment and update the ui
                     console.log(json.id);
                      $("#comment-" + json.id).remove();
                      $(".newbox").remove();

                 }


                })
                .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
                })

        }

        // ajax interaction for editing comments

       $(".commentbuttonbox").on("click",".edit-comment", function(event) {

             event.preventDefault();
                   var commentId = $(this).data("editcomment-id");
                 $(".editcomment").hide();
                  $(".commentbuttonbox").hide();
                 $("#commentbyauthor").hide();
                 $("#editcomment-" + commentId).show();


           });

    $(".pastcomments").on("click", ".savecomment", function (event) {
    event.preventDefault();

    // Accessing the comment edited by the user
    var commentId = $(this).data("savecomment-id");
    var comment = $("#editcommentbox-" + commentId).val();
    var commenturl = $(this).data("savecomment-url");
    console.log(commenturl);

    // Update comment using AJAX
    updatecomment(commenturl, comment, commentId);
});

        // function for saving and updating the comment on the UI using AJAX
        function updatecomment(commenturl,comment,commentId) {
            // sending ajax request with comment to be added as data
            $.ajax({
                url: commenturl,
                data: {
                    comment:comment,
                     commentId: commentId,
                },
                type: "POST",
                dataType: "json",
                headers: {'X-CSRFToken': csrftoken}

            })

            .done(function(json) {

                // updating the edited comment and displaying it.
                 if(json.success){
                     $("#commentbyauthor").text(json.message);
                     // var newcommentauthor='@ <a href="{% url "users:profile_detail" ' + json.author + ' %}">' + json.author + '</a> • ' + json.date;
                     // $("#commentauthor").html(newcommentauthor);

                // Show edit, delete buttons, and updated comment
                $(".commentbuttonbox").show();
                $("#commentbyauthor").show();
                 // Hide the edit form
                     console.log(json.id);
                $("#editcomment-" + json.id).hide();


                 }


                })
                .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
                })

        }


    // additional hover interactions for the categories navbar added for further customization
      $(".itemcategories").on("mouseover", ".categories", function()
      {
            $(this).css({"font-size": "1.1rem", "color": "var(--primary-color3)"});
            $(this).off("mouseover");

      });


     $(".itemcategories").on("mouseout", ".categories", function()
      {
            $(this).css({"font-size": "1rem", "color": "var(--primary-color)"});
            $(this).off("mouseout");

      });



     });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');