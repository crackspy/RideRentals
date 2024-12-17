const header = document.querySelector(".tabs__header");
const title = document.querySelector(".tabs__title");
const description = document.querySelector(".tabs__description");
const submitButton = document.querySelector(".tabs__button");
const tabs = header.children;

function updateTabContent(tabName) {
  const isLoginTab = tabName === "Login";

  title.innerText = isLoginTab
    ? "Login to Your Account"
    : "Create a New Account";
  description.innerText = isLoginTab
    ? "Welcome back! Please enter your credentials to access your account."
    : "Join us today! Fill out the form below to create a new account.";
  submitButton.value = isLoginTab ? "Log in" : "Register";

  tabs[0].classList.toggle("tabs__tab--active", isLoginTab);
  tabs[1].classList.toggle("tabs__tab--active", !isLoginTab);
}

header.addEventListener("click", (event) => {
  updateTabContent(event.target.textContent);
});