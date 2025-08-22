<template>
  <div class="mt-4">
   <div class="ms-2">
     <h6 class="mb-3 font-13 fw-bold">Password Policy</h6>
    <!-- Dropdown -->
    <select v-model="selectedScore" class="form-select shadow-sm w-25 font-14">
      <option value="" disabled>Select Score</option>
      <option value="2">Score 2 – Fair</option>
      <option value="3">Score 3 – Strong</option>
      <option value="4">Score 4 – Very Strong</option>
    </select>
   </div>

    <!-- Dynamic Card -->
    <div v-if="selectedDetails" class="card shadow-sm mt-4 border-0 rounded-3 font-13 ">
      <div class="card-body font-13">
        <!-- Header -->
        <div class="d-flex align-items-center gap-3">
          <h5 class="fw-bold m-0 font-14" >
            Score {{ selectedScore }} – {{ selectedDetails.title }}
          </h5>
          <!-- <span class="badge px-3 py-2" :class="{ 'bg-warning text-dark': selectedScore == 2, 'bg-success': selectedScore == 3, 'bg-primary': selectedScore == 4 }">
            {{ selectedDetails.title }}
          </span> -->
        </div>

        <!-- Meaning -->
        <p class="mt-3"><b>Meaning : </b> {{ selectedDetails.meaning }}</p>

        <!-- Examples -->
        <div class="mt-2">
          <b>Examples : </b>
          <ul class="mt-1 list-unstyled">
            <li v-for="(ex, i) in selectedDetails.examples" :key="i" class="text-muted">
              <i class="bi bi-key me-2 text-secondary"></i>{{ ex }}
            </li>
          </ul>
        </div>

        <!-- Characteristics -->
        <div class="mt-2">
          <b>Characteristics:</b>
          <ul class="mt-1 list-unstyled">
            <li v-for="(char, i) in selectedDetails.characteristics" :key="i" class="text-muted">
              <i class="bi bi-check-circle-fill me-2 text-success"></i>{{ char }}
            </li>
          </ul>
        </div>

        <!-- Crack Time -->
        <p class="mt-2">
          <b>⏳ Crack Time : </b>
          <span class="text-danger">{{ selectedDetails.crackTime }}</span>
        </p>
      </div>

        <div class="d-flex mb-3 ms-3">
            <button class="btn save-btn" data-bs-toggle="modal" data-bs-target="#SavePasswordModal">Save</button>
        </div>

    </div>

    <div v-if="selectedDetails" class="modal fade" id="SavePasswordModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Password Policy</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body font-14">
            Are you sure you want to save <strong>{{ selectedDetails.title }}</strong> Password Policy?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary font-13" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark font-13 text-white" @click="SavePasswordPolicy">Yes, Proceed</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const selectedScore = ref("");


const scoreDetails = {
  2: {
    title: "Fair",
    meaning: "Offers some protection but still guessable within hours.",
    examples: ["Mango@123", "Sunshine2024"],
    characteristics: [
      "8–10 characters",
      "Contains at least one uppercase, lowercase, number, special character",
      "Still uses common word patterns",
    ],
    crackTime: "Minutes to hours depending on attacker resources.",
  },
  3: {
    title: "Strong",
    meaning: "Hard to guess for most automated attacks; requires targeted cracking.",
    examples: ["Tr0ub4dor@Sky2024", "M!nD#St0rm88"],
    characteristics: [
      "10–14 characters",
      "Fully mixed: uppercase, lowercase, numbers, special characters",
      "Not a dictionary word",
      "No obvious patterns",
    ],
    crackTime: "Months to years for brute-force.",
  },
  4: {
    title: "Very Strong",
    meaning: "Extremely hard to guess or crack, even with advanced tools.",
    examples: ["Vx9@bL0!z#P2hR7$M1", "MyT1gerE@ts5C@rrot!"],
    characteristics: [
      "14+ characters",
      "Random mix of all character types",
      "No meaningful words or patterns",
      "Passphrases with unrelated words and symbols",
    ],
    crackTime: "Centuries or longer with brute-force.",
  },
};

const selectedDetails = computed(() => scoreDetails[selectedScore.value] || null);

const SystemSettingData = () => {
    const docName = "System Settings";
    const queryParams = {
        fields: JSON.stringify(["minimum_password_score"]),
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.data) {
                selectedScore.value=res.data.minimum_password_score;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

onMounted(()=>{
    SystemSettingData()
})

function SavePasswordPolicy(){
    const docName = "System Settings";
    axiosInstance
            .put(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, {
                minimum_password_score: selectedScore.value,
            })
            .then(() => {
                toast.success(`Password Policy Saved Successfully`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('SavePasswordModal'));
                    modal.hide();
                SystemSettingData();
            })
            .catch(() => {
                console.error("Failed to update Password Policy");
            });
}


</script>

<style scoped>
.card {
  transition: 0.3s ease-in-out;
}
.card:hover {
  /* transform: translateY(-3px); */
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}
ul {
  padding-left: 20px;
}
.save-btn{
    width: 10vw;
    background-color: #212529;
    color: white;
}
</style>
