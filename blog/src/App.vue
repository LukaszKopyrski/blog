<template>
  <div id="container">
    <TheHeader></TheHeader>
    <TheMain></TheMain>
    <TheFooter></TheFooter>
  </div>
</template>

<script setup>
import TheHeader from './components/header/TheHeader.vue';
import TheMain from './components/main/TheMain.vue';
import TheFooter from './components/footer/TheFooter.vue';
</script>

<style>
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  font-family: sans-serif;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
}
#container {
  display: grid;
  grid-template-rows: auto 1fr auto;
  width: 100%;
  min-height: 100vh;
}
</style>
