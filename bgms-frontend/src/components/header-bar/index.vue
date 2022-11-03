<template>

<header>
    <!-- Header Logo -->
    <!-- @TODO: add root link to go to the home page -->
   <a href="/">
    <figure class="logo" title="BGMS" @click="onClickLogo()">      
    </figure>
    </a>
    <!-- optional place to put more links -->
    <nav>
        <slot></slot>
    </nav>
</header>

</template>

<script src="./header-bar.js"></script>

<style scoped src="./header-bar.css"></style>
