export default function isAuthenticated() {
    const userName = sessionStorage.getItem("UserName"); // Check session storage
    const userId = document.cookie
        .split('; ')
        .find(cookie => cookie.startsWith('user_id='))
        ?.split('=')[1] || null; // Check cookies

    return !!(userName && userId); // Returns true if either is found
}


