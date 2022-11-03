<template>

<nav>
    <!-- Booking links -->
    <!-- @TODO make this dynamic, only rendering a group of routes -->
    <div class="link-group" v-for="route in routes" :key="route.path">
        <div class="mainlink">
            <a
                class="link"
                
            >
                <i class="fa" :class="route.meta.icon"></i>
                {{ route.meta.linkLabel }}
            </a>
        </div>

        <ul>
            <li class="sublink" v-for="subroute in route.children" :key="subroute.path">
                <router-link
                    class="link"
                    :to="{name: subroute.name}"
                >
                    <i class="fa" :class="subroute.meta.icon"></i>
                    {{ subroute.meta.linkLabel }}
                </router-link>
            </li>
        </ul>
    </div>

</nav>

</template>

<style scoped src="./nav-bar.css"></style>

<script src="./nav-bar.js"></script>
