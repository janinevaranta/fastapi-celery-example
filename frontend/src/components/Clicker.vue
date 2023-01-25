<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <button @click="count++">Click</button>
    <p>Try to click here 👆 while uploading large files.</p>
  </div>
</template>
