function validateChangeUsername(val) {
  var usernameReGEX = /^(?=.{8,20}$)(?![-_.0-9])(?!.*[_.-]{2})[a-zA-Z0-9._-]+(?<![_.-])$/;
  return usernameReGEX.test(val);
}
function validateChangeName(val) {
  var nameReGEX = /^[a-zA-Z][a-zA-Z][a-zA-Z]+(\s[a-zA-Z]+)?$/;
  return nameReGEX.test(val);
}
function validateChangeEmail(val) {
  var emailReGEX = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  return emailReGEX.test(val);
}

$("#inputChangeUsername").on("input", function() {
  if (validateChangeUsername($(this).val())) {
    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");
    $("#submitChangeUsername").attr("disabled", false);
  } else {
    $(this).removeClass("is-valid");
    $(this).addClass("is-invalid");
    $("#submitChangeUsername").attr("disabled", true);
  }
});

$("#inputChangeLastName").on("input", function() {
  if (validateChangeName($(this).val())) {
    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");
  } else {
    $(this).removeClass("is-valid");
    $(this).addClass("is-invalid");
  }
});
$("#inputChangeFirstName").on("input", function() {
  if (validateChangeName($(this).val())) {
    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");
  } else {
    $(this).removeClass("is-valid");
    $(this).addClass("is-invalid");
  }
});

$("#inputChangeEmail").on("input", function() {
  if (validateChangeEmail($(this).val())) {
    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");
    $("#submitChangeEmail").attr("disabled", false);
  } else {
    $(this).removeClass("is-valid");
    $(this).addClass("is-invalid");
    $("#submitChangeEmail").attr("disabled", true);
  }
});

$("#inputChangeBio").on("input", function() {
  console.log("hello");
  $("#bioCounter").text($(this).val().length + " Characters");
});
