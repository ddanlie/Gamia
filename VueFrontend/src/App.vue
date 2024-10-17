<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue';
// import HelloWorld from './components/HelloWorld.vue'



</script>

<script>
export default {
  mounted() {
    this.$router.push({ name: 'home' });
  }
}
</script>

<template>

      <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->


  <RouterView />
  <!-- <HomeView/> -->
</template>


<style>
h1 
{
  text-align: center;
}

body
{
  background-color: #FCEEDF;
}

ul
{
  list-style: none;
  margin: 0;
  padding: 0;
}

ul li
{
  margin: 0;
}

</style>
