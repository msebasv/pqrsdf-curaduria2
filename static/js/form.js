$(document).ready(function () {
  if ($("#id_type_identification :selected").text() == "---------") {
    $("#id_identification").hide();
  } else {
    $("#id_identification").show();
  }
  if ($("#id_medium_contact :selected").text() == "---------") {
    $("#id_email").hide();
    $("#id_correspondence_address").hide();
    $("#id_neighborhood").hide();
    $("#id_municipality").hide();
    $("#id_country").hide();
  }
  typePqrsdf();
  checkedAnonymous();
  selectTypeIdentificacion();
  selectMediumContact();
});

function typePqrsdf() {
  $("select#id_type_pqrsdf").on("change", function () {
    var valuePqrsdf = $(this).val();
    if (
      valuePqrsdf == "Peticion" ||
      valuePqrsdf == "Solicitud" ||
      valuePqrsdf == "Sugerencia"
    ) {
      $("#id_anon").hide();
    } else {
      $("#id_anon").show();
    }
  });
}

function checkedAnonymous() {
  var input = document.querySelector("input[class=form-check-input]");
  input.addEventListener("change", function () {
    if (input.checked) {
      $("#id_name").hide();
      $("#id_type_identification").hide();
      $("#id_identification").hide();
      $("#id_medium_contact").hide();
      $("#id_email").hide();
      $("#id_correspondence_address").hide();
      $("#id_neighborhood").hide();
      $("#id_municipality").hide();
      $("#id_country").hide();
      $("#id_number_contact").hide();
    } else {
      $("#id_name").show();
      $("#id_type_identification").show();
      $("#id_identification").show();
      $("#id_medium_contact").show();
      $("#id_email").show();
      $("#id_correspondence_address").show();
      $("#id_neighborhood").show();
      $("#id_municipality").show();
      $("#id_country").show();
      $("#id_number_contact").show();
    }
  });
}

function selectTypeIdentificacion() {
  $("select#id_type_identification").on("change", function () {
    if ($("#id_type_identification :selected").text() == "---------") {
      $("#id_identification").hide();
    } else {
      $("#id_identification").show();
    }
  });
}

function selectMediumContact() {
  $("select#id_medium_contact").on("change", function () {
    var value = $(this).val();
    if ($("#id_medium_contact :selected").text() == "---------") {
      $("#id_identification").hide();
      $("#id_correspondence_address").hide();
      $("#id_neighborhood").hide();
      $("#id_municipality").hide();
      $("#id_country").hide();
    } else if (value == "CE") {
      $("#id_email").show();
      $("#id_correspondence_address").hide();
      $("#id_neighborhood").hide();
      $("#id_municipality").hide();
      $("#id_country").hide();
    } else {
      $("#id_email").hide();
      $("#id_correspondence_address").show();
      $("#id_neighborhood").show();
      $("#id_municipality").show();
      $("#id_country").show();
    }
  });
}
