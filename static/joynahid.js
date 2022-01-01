let vjudgeHolder = `<div class="form-row pt-3">
<div class="col">
<input id="contest_ids_vj" aria-describedby="contest_ids_vj_help" class="form-control" type="text"
  placeholder="VJudge Contest ID" name="contest_ids_vj" value="">
</div>

<div class="col">
<input id="contest_ids_vj_passwords" aria-describedby="contest_ids_vj_passwords_help"
  class="form-control" type="text" placeholder="VJudge Contest Password" name="contest_ids_vj_passwords"
  value="">
</div>
</div>`;

let form = document.querySelector("form");
let addNewVj = document.getElementById("add_contest_vj");

addNewVj.addEventListener("click", (e) => {
  e.preventDefault();
  $("#vjudge_container").append(vjudgeHolder);
});

var yo = 0;

form.addEventListener("submit", (e) => {
  let worker = setInterval(() => {
    if (yo % 3 == 0) $("#working").html("Working.");
    else if (yo % 3 == 1) $("#working").html("Working..");
    else $("#working").html("Working...");

    yo++;
  }, 500);

  var ws = new WebSocket(
    "wss://" + document.domain + ":" + location.port + "/ws"
  );
  ws.onmessage = function (event) {
    $("#stream").append(`<li class="list-group-item"> > ${event.data}</li>`);
  };

  ws.onclose = function () {
    clearInterval(worker);
  };

  window.scrollTo(0, 0);

  $("#stream").html("");
  $(".loader").fadeIn(500);

  e.preventDefault();
  let formData = new FormData(document.querySelector("form"));

  let payload = {};

  formData.forEach((value, key) => {
    if (!(key in payload)) payload[key] = value + " ";
    else payload[key] += value + " ";
  });

  for (key in payload) {
    let value = payload[key];
    let str = value.slice(0, -1);
    payload[key] = str;
  }

  ws.onopen = function () {
    ws.send(JSON.stringify(payload));
  };
  return;

  $.ajax({
    type: "post",
    url: "/api/v1/generate_standings",
    data: payload,
    success: (response) => {
      let alrt = $(".alert");
      alrt.addClass("alert-success");
      $(".alert > p").html(
        `Successfully Updated in ${response} seconds. Please check <a target="__blank" href="${payload["up_sheet_link"]}">this google sheet.</a>`
      );
      $(".loader").hide();
      alrt.fadeIn("slow");
    },
    error: (error) => {
      let alrt = $(".alert");
      alrt.addClass("alert-danger");
      $(".alert > p").html(
        `Sorry! Something went wrong. Please fill all the information correctly`
      );
      $(".loader").hide();
      alrt.fadeIn("slow");
    },
  });
});
