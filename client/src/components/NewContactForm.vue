<template>
  <div align="left">
    <p class="h3 m-0">Lisa uus kontakt</p>
    <hr class="my-2" />
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-name"
        label="Nimi:"
        label-for="input-name"
        label-size="sm"
        label-class="p-0 m-0"
      >
        <b-form-input id="input-name" size="sm" v-model="form.name" required></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-codename"
        label="Koodnimi:"
        label-for="input-codename"
        label-size="sm"
        label-class="p-0 m-0"
      >
        <b-form-input id="input-codename" size="sm" v-model="form.codename" required></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-phone"
        label="Telefon:"
        label-for="input-phone"
        label-size="sm"
        label-class="p-0 m-0"
      >
        <b-form-input type="tel" id="input-phone" size="sm" v-model="form.phone" required></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="link" size="sm">
        <b-spinner v-if="loading" small></b-spinner>
        <div v-else>
          <font-awesome-icon icon="user-plus" size="lg"></font-awesome-icon>
          <p class="small d-inline-block mb-0 ml-2">Salvesta kontakt</p>
        </div>
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "NewContactForm",
  data() {
    return {
      form: {
        name: "",
        codename: "",
        phone: ""
      },
      show: true,
      loading: false
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.createContact();
    },
    onReset(evt) {
      evt.preventDefault();
      this.resetForm();
    },
    resetForm() {
      this.form.name = "";
      this.form.codename = "";
      this.form.phone = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    createContact() {
      this.loading = true;
      this.$http({
        method: "post",
        url: this.$apiBaseUrl + "/api/contacts/",
        headers: { Authorization: this.$store.getters.bearerToken },
        data: {
          id: null,
          name: this.form.name,
          codename: this.form.codename,
          phone: this.form.phone
        }
      })
        .then(resp => {
          if (resp.data) {
            this.$emit("addContactSuccess", resp.data);
            this.resetForm();
          }
          this.loading = false;
        })
        .catch(err => {
          this.loading = false;
        });
    }
  }
};
</script>

