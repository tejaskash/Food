// Wait for the DOM to be ready
$(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='registration']").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        fname: {
            required:true,
            number:true

        },
        lname: "required",
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        psw: {
          required: true,
          minlength: 5
        },
        pincode: {
          required: true,
          minlength: 6,
          maxlength: 6
        },
      },
      // Specify validation error messages
      messages: {
        fname: "Please enter your Unit Name",
        lname: "Please enter your lastname",
        psw: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        email: "Please enter a valid email address",
        pincode:
        {
            required:"Please enter a pincode",
            minlength:"At Least 6 characters",
            maxlength:"Atmost 6 characters"

        }
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
        form.submit();
      }
    });
  });