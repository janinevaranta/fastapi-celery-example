<script setup lang="ts">
import UploadExcel from "./components/UploadExcel.vue";
import Clicker from "./components/Clicker.vue";

const base_url = "/backend";
const endpoints = {
  easy: "/task/easy",
  medium: "/task/medium",
  hard: "/task/hard",
  excel: "/task/excel/uploadfile",
  pollingExcel: "/task/excel/uploadfile_with_progress"
};
</script>

<template>
  <div class="container">
    <Clicker></Clicker>
    <UploadExcel :url="base_url + endpoints.excel" :polling-url="base_url + endpoints.pollingExcel" />
  </div>
</template>

<style>
.container {
  display: flex;
  flex-direction: row;
  gap: 5em;
  width: 80vw;
}
</style>