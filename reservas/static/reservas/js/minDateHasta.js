function minDateHasta() {
    var minDate = document.getElementById('date-desde').valueOf();
    minDate = minDate.value;
    console.log(minDate);
    document.getElementById("date-hasta").setAttribute("type", 'date');
    document.getElementById("date-hasta").setAttribute('min', minDate);
}