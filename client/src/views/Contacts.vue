<template>
  <div class="container">
    <Navbar @toggleNewUser="toggleNewUser" />
    <div v-if="loading" class="mt-4 pt-4">
      <b-spinner variant="primary" label="Spinning"></b-spinner>
    </div>
    <div v-else>
      <b-collapse id="new-user-collapse" v-model="newUserMode" class="mt-2 shadow-sm">
        <b-card>
          <NewContactForm @addContactSuccess="addContact" />
        </b-card>
      </b-collapse>
      <b-list-group flush class="mt-2">
        <b-list-group-item v-for="contact in contacts" :key="contact.id" class="border-0 py-1">
          <Contact :contact="contact" @deleteSuccess="removeContact" />
        </b-list-group-item>
      </b-list-group>
      <b-pagination
        v-if="(totalElements > pageSize)"
        v-model="currentPage"
        class="mt-2"
        :total-rows="totalElements"
        :per-page="pageSize"
        align="center"
        size="sm"
        @input="fetchContacts"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Contact from "@/components/Contact.vue";
import NewContactForm from "@/components/NewContactForm.vue";

export default {
  name: "Contacts",
  components: {
    Navbar,
    Contact,
    NewContactForm
  },
  data() {
    return {
      newUserMode: false,
      pageSize: 10,
      currentPage: 1,
      direction: "asc",
      orderBy: "createdAt",
      loading: false,
      contacts: [],
      totalPages: 0,
      totalElements: 0
    };
  },
  methods: {
    openNewUser() {
      this.newUserMode = true;
    },
    closeNewUser() {
      this.newUserMode = false;
    },
    toggleNewUser() {
      this.newUserMode = !this.newUserMode;
    },
    fetchContacts() {
      this.loading = true;
      this.$http({
        method: "get",
        url: this.$apiBaseUrl + "/api/contacts/",
        params: { page: this.currentPage },
        headers: { Authorization: this.$store.getters.bearerToken }
      })
        .then(resp => {
          this.contacts = resp.data.results;
          this.totalPages = resp.data.totalPages;
          this.totalElements = resp.data.count;
          this.loading = false;
        })
        .catch(err => {
          this.loading = false;
        });
    },
    addContact(contact) {
      if (this.contacts.length >= this.pageSize) {
        this.contacts.shift();
      }
      this.contacts.unshift(contact);
    },
    removeContact(id) {
      for (var i = 0; i < this.contacts.length; i++) {
        if (this.contacts[i].id == id) {
          this.contacts.splice(i, 1);
          break;
        }
      }
    }
  },
  mounted() {
    this.fetchContacts();
  }
};
</script>

