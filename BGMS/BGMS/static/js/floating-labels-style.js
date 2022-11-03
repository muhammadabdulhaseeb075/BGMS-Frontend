$(function() {
  //$("body").on("input propertychange", ".floating-label-form-group", function(e) {
  $("body").on("focus", ".floating-label-form-group-style", function() {
    $(this).addClass("floating-label-form-group-style-with-focus");
  }).on("blur", ".floating-label-form-group-style", function() {
    $(this).removeClass("floating-label-form-group-style-with-focus");
  });
});
