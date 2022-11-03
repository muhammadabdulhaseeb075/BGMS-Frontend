<template>
<div id="app">
    <header-bar>
        <user-info></user-info>
        <div class="p-2 mr-6 cursor-pointer"><a href="https://bgmssign.s3.eu-west-1.amazonaws.com/docs/BGMS_Booking_User_Guide.pdf" target="_blank">User Guide</a></div>
        <div class="p-2 mr-6 cursor-pointer" @click="logout()">
            Log Out
        </div>
    </header-bar>
    <div class="content">
        <side-bar>
            <nav-bar></nav-bar>
            <site-select :inline="false" @setSiteSelectVisibility="handleSiteSelectVisibilityEvent"></site-select>
        </side-bar>
        <main>
            <router-view></router-view>
        </main>
    </div>
    <div id="modals-teleport"></div>
</div>
</template>

<style scoped>
@import "styles/theme.css";

#app {
    @apply flex flex-col;
    height: auto;
    min-height: inherit;

    .content {
        @apply flex;

        flex-grow: 1;
    }

    main {
        background-color:white;
        margin-left: $sidebar-width;
        margin-top: $header-height;
        max-height: calc(100% - $header-height);
        position: relative;
        width: calc(100% - $sidebar-width);
    }
}
</style>

<script>
import { useStore, mapActions } from "vuex";

import HeaderBar from "src/components/header-bar";
import SideBar from "src/components/side-bar";
import NavBar from "src/containers/nav-bar";
import UserInfo from "src/containers/user-info";
import SiteSelect from "src/containers/site-select";

function data() { return {};}

function setup() {
    const store = useStore();
    return {
        title: store.state.title,
    };
}

const methods = {
    ...mapActions([
        "logout",
    ]),
};

const computed = {
};

const mounted = () => {
};

const components = {
    HeaderBar,
    SideBar,
    NavBar,
    UserInfo,
    SiteSelect,
};

export default {
    name: "app",
    data,
    setup,
    methods,
    computed,
    mounted,
    components,
};
</script>
