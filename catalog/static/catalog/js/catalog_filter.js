const searchForm = document.getElementById("searchFormValue"); // считываем форму

const allCards = document.querySelectorAll(".my-card-col");

searchForm.addEventListener("input", inputHandler);

addEventListener("keydown", (e) => {
  // не срабатывает enter
  if (e.key === "Enter") e.preventDefault();
});

function inputHandler() {
  const inputValue = searchForm.value;

  allCards.forEach((card) => {
    const thisCardTitle = card.querySelector(".card-title").textContent;

    if (
      thisCardTitle.toLowerCase().indexOf(inputValue.toLowerCase()) != -1
    ) {
      card.classList.remove("hide-card");
    } else {
      card.classList.add("hide-card");
    }
  });
}