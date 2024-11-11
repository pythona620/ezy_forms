export default function isAuthenticated() {
    return !!localStorage.getItem("UserName"); // Assuming you store login info in localStorage
}