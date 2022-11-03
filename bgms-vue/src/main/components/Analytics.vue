<template>
  <vue-cookie-accept-decline
    :ref="'myPanel1'"
    :elementId="'myPanel1'"
    :debug="false"
    position="bottom"
    :disableDecline="false"
    :transitionName="'slideFromBottom'"
    :showPostponeButton="false"
    @status="processInitialStatus"
    @clicked-accept="enableAnalytics">

    <!-- Optional -->
    <div slot="postponeContent">
      &times;
    </div>

    <!-- Optional -->
    <div slot="message">
      We use cookies to ensure you get the best experience on our website. Read our <a href="https://www.atlanticgeomatics.co.uk/user_uploads/privacy-policy.pdf" target="_blank">Cookie Policy</a> to learn more.
    </div>

    <!-- Optional -->
    <div slot="declineContent">
      OPT OUT
    </div>

    <!-- Optional -->
    <div slot="acceptContent">
      GOT IT!
    </div>
  </vue-cookie-accept-decline>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import 'vue-cookie-accept-decline/dist/vue-cookie-accept-decline.css'
import VueCookieAcceptDecline from 'vue-cookie-accept-decline'
import VueGtag from "vue-gtag";

Vue.use(VueGtag, {
  config: { id: process.env.VUE_APP_GOOGLE_ANALYTICS_KEY },
  enabled: false
});

@Component({
  components: {
    VueCookieAcceptDecline,
  }
})
export default class Analytics extends Vue {

  /**
   * Called when component is created. If cookies have already been accepted, status will be 'accept'
   */
  processInitialStatus(status) {
    if (status === "accept")
      this.enableAnalytics();
  }

  /**
   * Enabled Google Analytics
   */
  enableAnalytics() {
    this.$gtag.optIn();
  }
  
}
</script>