"use strict";

const $submitButton = $("#create-cupcake");


async function addCupcake() {


  const response = await axios.post("/api/cupcakes",
  params: {$("#flavor").val(), $("#size"), )
}

$submitButton.on("click", addCupcake);
