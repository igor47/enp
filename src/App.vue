<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import NumberInput from './components/NumberInput.vue'
</script>

<template>
  <h2>
    Thank you for using the Evergrow Number Printer.
    Please enter some numbers, and click "Print" to print them to a PDF file.
  </h2>

  <NumberInput />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
