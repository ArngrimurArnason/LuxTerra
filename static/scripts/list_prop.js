
function changeQty(btn, delta) {
const input = btn.parentElement.querySelector('input');
let val = parseInt(input.value) || 0;
val = Math.max(0, val + delta);
input.value = val;
}


function previewThumbnail(input) {
const preview = document.getElementById("thumbnail-preview");
const img = document.getElementById("thumb-img");

if (input.files && input.files[0]) {
  const reader = new FileReader();
  reader.onload = function (e) {
    img.src = e.target.result;
    preview.style.display = "block";
  };
  reader.readAsDataURL(input.files[0]);
} else {
  preview.style.display = "none";
}
}
