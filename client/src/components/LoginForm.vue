<template>
  <div>
    <p v-if="errorMessage != ''" class="text-danger lead mb-2">{{errorMessage}}</p>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-username"
        label="Kasutajanimi:"
        label-for="input-username"
        label-size="sm"
        label-align="left"
        label-class="p-0 m-0"
      >
        <b-form-input id="input-username" v-model="form.username" type="text" required></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-password"
        label="Salasõna:"
        label-for="input-password"
        label-size="sm"
        label-align="left"
        label-class="p-0 m-0"
      >
        <b-form-input id="input-password" v-model="form.password" type="password" required></b-form-input>
      </b-form-group>
      <b-button type="submit" size="sm" variant="primary">
        <b-spinner v-if="authStatus == 'loading'" small></b-spinner>
        <span v-else>Sisene</span>
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      show: true,
      errorMessage: ""
    };
  },
  methods: {
    onSubmit(evt) {
      this.loading = true;
      evt.preventDefault();
      this.$store
        .dispatch("login", this.form)
        .then(() => {
          this.errorMessage = "";
          this.$router.push("contacts");
        })
        .catch(err => {
          this.errorMessage = "Vale kasutajanimi või parool!";
        });
    },
    onReset(evt) {
      evt.preventDefault();
      this.form.username = "";
      this.form.password = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  },
  computed: {
    authStatus() {
      return this.$store.getters.authStatus;
    }
  }
};
</script>