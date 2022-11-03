<template>
  <v-app id="MainBookingApp">

    <Analytics></Analytics>

    <div class="top-nav">
      <header class="navbar navbar-expand-lg navbar-light" role="navigation">
        <v-row no-gutters>
          <v-col sm="4">
             <router-link to="/">
              <a href="/">
                <img class="logo" :src="require('@/mapmanagement/static/images/BGMS_logo_header.png')" crossorigin="anonymous" />
              </a>
            </router-link>
          </v-col>
           <v-col sm="8">
               <div class="d-flex align-right justify-end">
                 <a href="/logout/" nav>
                      <v-btn
                        dark
                        text>
                          <span>Log Out</span>
                      </v-btn>
               </a>
            </div>
           </v-col>
        </v-row>
      </header>
	</div>

    <div class="d-flex flex-grow-1 content-area">
      <div class="main-sidebar">
        <!-- sidebar: style can be found in sidebar.less -->
        <div class="sidebar" id="scrollspy">

          <v-menu bottom content-class="user-menu">
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                text
                v-on="on">
                <i class="fas fa-user"/>
                <span><i class="user-menu-user">{{ username }}</i></span>
                <i class="fas fa-caret-down"/>
              </v-btn>
            </template>
            <v-list>
              <v-list-item tag="a" href="/logout/" nav>
                <v-list-item-title>Log Out</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <!-- sidebar menu: : style can be found in sidebar.less -->
          <ul class="nav sidebar-menu" style="height: 300px">
                <li class="button-link-wrapper">
                    <a class="button-link-parent" href="#/">
                        <i class="fa fa-calendar"></i>
                       Bookings
                    </a>
                </li>
                <li class="button-link-wrapper button-link-child">
                    <a class="button-link" href="#/add-booking">
                       <i class="fa fa-plus"></i>
                       New Booking
                    </a>
                </li>
          </ul>

          <SiteList></SiteList>          
          
        </div>
        <!-- /.sidebar -->
      </div>

      <div class="main-contents">
            <router-view></router-view>
      </div>
   </div>


    <v-footer class="page-footer" color="grey lighten-2">
      <v-row>
        <v-col cols="4" class="copyright py-0">
          © {{new Date().getFullYear()}} Atlantic Geomatics (Int'l) Limited
        </v-col>
        <v-col cols="4" class="text-center py-0">
          <a href="https://www.atlanticgeomatics.co.uk" target="_blank">
            <img style="vertical-align: middle" :src="require('@/mapmanagement/static/images/ag-logo.png')" crossorigin="anonymous" />
          </a>
        </v-col>
        <v-col cols="4" class="text-right py-0">
          <!--<v-btn text target="_blank" href="/docs/BGMS_User_Guide.pdf">USER GUIDE</v-btn>-->
        </v-col>
      </v-row>
    </v-footer>

  </v-app>
</template>

<script  lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import Analytics from '@/main/components/Analytics.vue';
import BookingMenu from "@/main-booking/components/BookingMenu.vue";
import SiteList from "@/main-booking/components/Forms/SiteList.vue";

@Component({
  components: {
    Analytics,
    BookingMenu,
    SiteList
  }
})
export default class MainBooking extends Vue {

  get username() {
    return (window as any).document.user.username;
  }
}
</script>

<style>
    .content-area {
        position: relative;
    }

    .main-sidebar {
        background-color: #c3af42;
        position: fixed;
        overflow: hidden;
        min-height: 100vh;
        display: block;
    }

    .page-footer {
      z-index: 999;
    }

    .main-contents {
         height: 100%;
        margin-left: 230px;
        width: calc(100% - 230px);
    }

    .sidebar-menu > .button-link-wrapper {
        padding: 5px;
    }

    .sidebar-menu > .button-link-child {
        padding: 5px 5px 5px 20px;
    }


    .sidebar-menu > .button-link-wrapper > .button-link-parent {
        padding: 8px 20px;
        border-radius: 5px;
        color: black;
        background-color: orangered;
        opacity: 0.8;
    }

    .sidebar-menu > .button-link-wrapper > .button-link {
        padding: 8px 20px;
        border-radius: 5px;
        color: black;
    }


    .sidebar-menu > .button-link-wrapper > .button-link {
        padding: 8px 20px;
        border-radius: 5px;
        color: black;
    }

    .skin-bgms .sidebar-menu>li.active> .button-link , .skin-bgms .sidebar-menu>li:hover> .button-link {
        border-left-color: transparent;
        border-left: none;
    }

    .skin-bgms .sidebar-menu>li.active.button-link-child > .button-link,
    .skin-bgms .sidebar-menu>li:hover.button-link-child > .button-link {
        background: white;
    }

</style>