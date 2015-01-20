$.ajax({
  url: '/add_to_log',
  async: true,
  dataType: 'html',
  type: "GET",
  cache: false,
  success: function (data) {
    var previousWorkouts = JSON.parse(data);
    for (var i = 0; i < previousWorkouts.length; i++) {
        var workout = previousWorkouts[i];
        $(".last-workouts").append("<tr><td>" + workout.name + "</td><td>" +  workout.reps + "</td><td>" +   workout.sets + "</td></tr>");
    }
  }
});

$(document).on("click", ".last-workouts tr", function() {
  var workoutData, setsData, repsData;
  workoutData = $(this).find("td:first").text();
  setsData = $(this).find("td:eq(1)").text();
  repsData = $(this).find("td:last").text();
  fillInData(workoutData, setsData, repsData);
});

function fillInData(workout, sets, reps) {
  var workoutInput, setsInput, repsInput;
  workoutInput = $("#existing-log-workout");
  setsInput = $("#existing-log-sets");
  repsInput = $("#existing-log-reps");
  workoutInput.val(workout);
  setsInput.val(sets);
  repsInput.val(reps);
}
