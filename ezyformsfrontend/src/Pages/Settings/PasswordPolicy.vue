<template>
  <div class="mt-4">
    <div class="ms-2 mb-3">
      <h6 class="font-13 fw-bold">Password Policy</h6>
    </div>

    <!-- All Score Cards in One Row -->
    <div class="row g-4 p-3">
      <div v-for="(details, score) in scoreDetails" :key="score" class="col-md-4 col-sm-12">
        <div class="card border-0 rounded-3 font-13 h-100">
          <div class="card-body font-13 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="fw-bold font-16 mb-2">
                  {{ details.title }}
                </h5>

                <!-- Conditional Button -->
                <span v-if="Number(selectedScore) === Number(score)" class="selected-btn" disabled>
                  ✅ Selected
                </span>
                <span v-else class="save-btn" data-bs-toggle="modal" data-bs-target="#SavePasswordModal"
                  @click="selectPolicy(score)">
                  Set as Default
                </span>
              </div>

              <!-- Meaning -->
              <p class="mt-2"><b>Meaning :</b> {{ details.meaning }}</p>

              <!-- Examples -->
              <div class="mt-2">
                <b>Examples :</b>
                <ul class="mt-1 list-unstyled">
                  <li v-for="(ex, i) in details.examples" :key="i" class="text-muted">
                    <i class="bi bi-key me-2 text-secondary"></i>{{ ex }}
                  </li>
                </ul>
              </div>

              <!-- Characteristics -->
              <div class="mt-2">
                <b>Characteristics :</b>
                <ul class="mt-1 list-unstyled">
                  <li v-for="(char, i) in details.characteristics" :key="i" class="text-muted">
                    <i class="bi bi-check-circle-fill me-2 text-success"></i>{{ char }}
                  </li>
                </ul>
              </div>

              <!-- Crack Time -->
              <p class="mt-2">
                <b>⏳ Crack Time :</b>
                <span class="text-danger ms-2">{{ details.crackTime }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Confirmation Modal -->
    <div v-if="selectedScore" class="modal fade" id="SavePasswordModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Password Policy</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body font-14">
            Are you sure you want to set
            <strong>{{ scoreDetails[pendingScore]?.title }}</strong> Password
            Policy as Default?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary font-13" data-bs-dismiss="modal">
              Cancel
            </button>
            <button type="button" class="btn btn-dark font-13 text-white" @click="SavePasswordPolicy">
              Yes, Proceed
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { showSuccess } from "../../shared/services/toast";

const selectedScore = ref("");
const pendingScore = ref("");

const scoreDetails = {
  2: {
    title: "Fair",
    meaning: "Offers some protection but still guessable within hours.",
    examples: ["Mango@123", "Sunshine2024"],
    characteristics: [
      "8–10 characters",
      "Contains uppercase, lowercase, number, special character",
      "Uses common word patterns",
    ],
    crackTime: "Minutes to hours depending on attacker resources.",
  },
  3: {
    title: "Strong",
    meaning:
      "Hard to guess for most automated attacks; requires targeted cracking.",
    examples: ["Tr0ub4dor@Sky2024", "M!nD#St0rm88"],
    characteristics: [
      "10–14 characters",
      "Mix of uppercase, lowercase, numbers, special characters",
      "Not a dictionary word",
      "No obvious patterns",
    ],
    crackTime: "Months to years for brute-force.",
  },
  4: {
    title: "Very Strong",
    meaning:
      "Extremely hard to guess or crack, even with advanced tools.",
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

const SystemSettingData = () => {
  const docName = "System Settings";
  const queryParams = {
    fields: JSON.stringify(["minimum_password_score"]),
  };

  axiosInstance
    .get(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, { params: queryParams })
    .then((res) => {
      if (res.data) {
        selectedScore.value = res.data.minimum_password_score;
      }
    })
    .catch((error) => {
      console.error("Error fetching system settings:", error);
    });
};

onMounted(() => {
  SystemSettingData();
});

function selectPolicy(score) {
  pendingScore.value = score; // store score to confirm in modal
}

function SavePasswordPolicy() {
  const docName = "System Settings";
  axiosInstance
    .put(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, {
      minimum_password_score: pendingScore.value,
    })
    .then(() => {
      showSuccess(`Password Policy Saved Successfully`);
      const modal = bootstrap.Modal.getInstance(document.getElementById("SavePasswordModal"));
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
  box-shadow: 0 6px 15px rgba(42, 41, 41, 0.15);
}

.card:hover {
  box-shadow: 0 6px 15px rgba(12, 11, 11, 0.15);
}

.save-btn {
  background-color: #c3c3c3;
  color: black;
  transition: 0.3s;
  padding: 5px 10px;
  border-radius: 10px !important;
  border: none;
  font-size: 12px;
}

.save-btn:hover {
  background-color: #3e3c3c;
  color: white;
}

.selected-btn {
  background-color: #6cc35b;
  color: #fff;
  padding:5px 10px;
  border-radius: 10px;
  border:none;
  font-size: 12px;
  cursor: default;
}
</style>
