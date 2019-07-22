import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faUserCog, faSignOutAlt, faAddressBook, faEdit, faTrashAlt, faUser, faUserPlus, faSave, faHistory, faUndo, faBackspace, faBan, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret, faUserCog, faSignOutAlt, faAddressBook, faEdit, faTrashAlt, faUser, faUserPlus, faSave, faHistory, faUndo, faBackspace, faBan, faCheck )

Vue.component('font-awesome-icon', FontAwesomeIcon)
