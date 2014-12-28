$("#search").keyup(function() {
  var query;
  query = $(this).val();
  $.get('/search', {"suggestion": query}, function(data) {
    $(".logs").html(data);
  });
});
