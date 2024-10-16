<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue';
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>

      <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->


  <!-- <RouterView /> -->
  <HomeView/>
</template>


<style>
h1 
{
  text-align: center;
}

</style>
