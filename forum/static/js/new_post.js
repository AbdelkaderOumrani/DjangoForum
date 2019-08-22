$(".category-element").click(function(target) {
  $("#post_category_name").val($(this).val());
  $("#post_category_id").val(
    $(this)
      .attr("id")
      .substring(4)
  );
  $("#categoriesModal").modal("hide");
});

/*Handle file input form */
$("#attach_file").change(function() {
  var fileName = $(this)
    .val()
    .split("\\")
    .pop();
  $(this)
    .siblings(".custom-file-label")
    .addClass("selected")
    .html(fileName);
});
/*End Handle file input form */

/*handle Post submit */
$("#new_post_form").submit(function() {
  $("#post_body").val($("#summernote").summernote("code"));
});

/*End handle Post submit */
