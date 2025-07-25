<template>
  <div class="app-div">
    <!-- Conditionally show the loader -->
    <LoaderPage v-if="loadValue"></LoaderPage>
    <section>


      <!-- Conditionally show the header and sidebar if not on '/new/formsteps' -->
      <!-- <HeaderComp v-if="!isFormStepsRoute" /> -->

      <div class="container-fluid p-0">
        <div class="row">
          <!-- Conditionally render the sidebar based on the current route -->
          <!-- <div class="col-2 p-0" v-if="!isFormStepsRoute && !isArchivedRoute">
            <SideBar />
          </div> -->

          <!-- Adjust column size based on route -->
          <!-- :class="[(isFormStepsRoute || isArchivedRoute) ? 'col-12' : 'col-10']" -->

          <RouterView></RouterView>

        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed, ref, watchEffect } from 'vue';
import HeaderComp from './Components/HeaderComp.vue';
import LoaderPage from './Components/loader/LoaderPage.vue';
import SideBar from './Components/SideBar.vue';
import '@vueform/multiselect/themes/default.css';
import { loadValue } from './Components/loader/loader'
import { watch } from 'vue';
import { onMounted } from 'vue';
// import { onBeforeUnmount } from 'vue';
// import axiosInstance from './shared/services/interceptor';
// import { apis } from './shared/apiurls';
// Get current route
const route = useRoute();
// let inactivityTimer

// const logoutUser = async () => {
//   try {
//     await axiosInstance.post(apis.logout)
    
//     // Clear all cookies
//     document.cookie.split(";").forEach(cookie => {
//       document.cookie = cookie
//         .replace(/^ +/, "")
//         .replace(/=.*/, `=;expires=${new Date(0).toUTCString()};path=/`)
//     })

//     window.location.href = '/login' // Redirect to login page
//   } catch (err) {
//     console.error('Logout failed:', err)
//   }
// }
// // const resetInactivityTimer = () => {
// //   clearTimeout(inactivityTimer)
// //   inactivityTimer = setTimeout(logoutUser, 20 * 1000) // ⏱️ 20 seconds for testing
// // }
// const resetInactivityTimer = () => {
//   clearTimeout(inactivityTimer)
//   inactivityTimer = setTimeout(logoutUser, 5 * 60 * 1000) // 5 minutes
// }

// onMounted(() => {
//   window.addEventListener('mousemove', resetInactivityTimer)
//   window.addEventListener('keydown', resetInactivityTimer)

//   resetInactivityTimer() // Start the initial timer
// })

// onBeforeUnmount(() => {
//   window.removeEventListener('mousemove', resetInactivityTimer)
//   window.removeEventListener('keydown', resetInactivityTimer)
//   clearTimeout(inactivityTimer)
// })
// Check if the current route is '/archived'
const isArchivedRoute = computed(() => route.path.startsWith('/archived'));

// Check if the current route is '/new/formsteps'
const isFormStepsRoute = computed(() => route.path.includes('/create-form/formsteps'));

const user_id = ref("");

// Function to get user_id from cookies
function getUserIdFromCookies() {
    return document.cookie
        .split("; ")
        .find((cookie) => cookie.startsWith("user_id="))
        ?.split("=")[1] || null;
}


function removeUserIdCookie() {
    document.cookie = "user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
    document.cookie = "full_name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
    user_id.value = ""; // Clear the reactive variable
    // console.log("user_id cookie removed");
}

// Function to remove user-related localStorage data
function clearLocalStorage() {
    localStorage.removeItem("UserName");
    localStorage.removeItem("employeeData");
    localStorage.removeItem("Bu");
    localStorage.removeItem("USERROLE");
    // console.log("Local storage cleared");
}

// Set the initial value on component mount
onMounted(() => {
    user_id.value = getUserIdFromCookies();
});

// Watch for changes in `sessionStorage` UserName
watchEffect(() => {
    const userName = sessionStorage.getItem("UserName");

    if (!userName) {
        clearLocalStorage();
        removeUserIdCookie();
    }
});
</script>

<style>
@media (min-width: 1604px) and (max-width: 2400px) {
  .col-2 {
    width: 13.33%;
  }

  .col-10 {
    width: 85.777%;
  }

  .col-12 {
    width: 100%;
  }
}

.app-div {
  overflow-x: hidden;
}
</style>
