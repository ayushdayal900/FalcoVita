<template>
  <div class="auth-container">
    <h2>Register</h2>

    <form @submit.prevent="handleRegister">

      <input
        v-model="form.name"
        type="text"
        placeholder="Full Name"
        required
      />

      <input
        v-model="form.email"
        type="email"
        placeholder="Email"
        required
      />

      <input
        v-model="form.password"
        type="password"
        placeholder="Password"
        required
      />

      <input
        v-model="form.contact_number"
        type="text"
        placeholder="Contact Number"
      />

      <!-- Role dropdown -->
      <select v-model="form.role" required>
        <option disabled value="">Select Role</option>
        <option value="doctor">Doctor</option>
        <option value="patient">Patient</option>
      </select>

      <!-- Doctor Fields -->
      <div v-if="form.role === 'doctor'">
        <input
          v-model="form.department_id"
          type="number"
          placeholder="Department ID"
          required
        />

        <input
          v-model="form.specialization"
          type="text"
          placeholder="Specialization"
          required
        />

        <input
          v-model="form.qualifications"
          type="text"
          placeholder="Qualifications"
          required
        />

        <input
          v-model="form.experience"
          type="number"
          placeholder="Experience (years)"
          required
        />
      </div>

      <!-- Patient Fields -->
      <div v-if="form.role === 'patient'">
        <input v-model="form.dob" type="date" required />

        <input
          v-model="form.contact"
          type="text"
          placeholder="Contact"
          required
        />

        <input
          v-model="form.medical_record_number"
          type="text"
          placeholder="Medical Record Number"
          required
        />

        <input
          v-model="form.doctor_id"
          type="number"
          placeholder="Doctor ID (optional)"
        />
      </div>

      <button type="submit">Register</button>
    </form>

    <p>
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Register",

  data() {
    return {
      form: {
        name: "",
        email: "",
        password: "",
        contact_number: "",
        role: "",

        // Doctor Fields
        department_id: "",
        specialization: "",
        qualifications: "",
        experience: "",

        // Patient Fields
        dob: "",
        contact: "",
        medical_record_number: "",
        doctor_id: "",
      },
      error: "",
    };
  },

  methods: {
    ...mapActions("auth", ["register"]),

    async handleRegister() {
      this.error = "";

      try {
        await this.register(this.form);

        alert("Registration Successful!");
        this.$router.push("/login");
      } catch (err) {
        this.error =
          err.response?.data?.message || "Registration failed. Try again.";
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 350px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
}

input,
select {
  width: 90%;
  padding: 10px;
  margin: 10px auto;
  display: block;
}

button {
  width: 95%;
  padding: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 12px;
}
</style>
