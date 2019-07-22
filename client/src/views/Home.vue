<template>
  <div class="container">
    <div class="d-flex justify-content-center" style="height: 80vh">
      <div class="my-auto shadow border px-4 py-2">
        <h1 class="display-4">
          <font-awesome-icon icon="address-book" class="mr-2" />Kontaktid
        </h1>
        <hr class="my-2" />
        <div v-if="formMode == 'login'">
          <p class="small text-muted">Kasutamiseks peate olema sisse logitud</p>
          <LoginForm />
          <p class="small mt-4 text-muted">
            Puudub kasutaja?
            <b-link href="#" @click="formMode = 'signup'">Registreeri</b-link>
          </p>
        </div>
        <div v-else-if="formMode == 'signup'">
          <p class="small text-muted">Registreeri uus kasutaja</p>
          <SignupForm
            @registrationSuccess="onRegistrationSuccess"
            @registrationSuccessContinue="onRegistrationSuccessContinue"
          />
          <p v-if="!registrationSuccess" class="small mt-4 p-0 text-muted">
            Kasutaja olemas?
            <b-link href="#" v-if="!registrationSuccess" @click="formMode = 'login'">Sisene</b-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import SignupForm from "@/components/SignupForm.vue";

export default {
  name: "Home",
  components: {
    LoginForm,
    SignupForm
  },
  data() {
    return {
      formMode: "login",
      registrationSuccess: false
    };
  },
  mounted() {
    if (this.$store.getters.isAuthenticated) {
      this.$router.push("contacts");
    }
  },
  methods: {
    onRegistrationSuccess() {
      this.registrationSuccess = true;
    },
    onRegistrationSuccessContinue() {
      this.registrationSuccess = false;
      this.formMode = "login";
    }
  }
};
</script>

<style lang="less" scoped>
</style>

