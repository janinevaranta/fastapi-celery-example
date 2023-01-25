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
  <Clicker></Clicker>
  <UploadExcel :url="base_url + endpoints.excel" :polling-url="base_url + endpoints.pollingExcel" />
</template>