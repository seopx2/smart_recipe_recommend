let ingredients = [];

function addIngredient() {
  const input = document.getElementById("ingredient-input");
  const value = input.value.trim();

  if (value && !ingredients.includes(value)) {
    ingredients.push(value);
    updateList();
  }

  input.value = "";
}

function updateList() {
  const list = document.getElementById("ingredient-list");
  list.innerHTML = "";

  ingredients.forEach((ing, index) => {
    const li = document.createElement("li");
    li.innerHTML = `${ing} <span onclick="removeIngredient(${index})">X</span>`;
    list.appendChild(li);
  });
}

function removeIngredient(index) {
  ingredients.splice(index, 1);
  updateList();
}

function startRecommendation() {
  // 다음 페이지로 이동하면서 재료 정보 전달
  const query = ingredients.map(i => encodeURIComponent(i)).join(',');
  window.location.href = `/result?ings=${query}`;

}
