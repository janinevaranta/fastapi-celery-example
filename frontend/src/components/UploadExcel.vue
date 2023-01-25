<script setup lang="ts">
import axios, { RawAxiosRequestConfig } from "axios";
import type { AxiosResponse } from "axios"
import FileDownload from "js-file-download";
import { ref, defineProps } from "vue";
import { useFileDialog } from "@vueuse/core";

// PROPS AND STATES
const props = defineProps(["url", "pollingUrl"])
const loading = ref(false);
// Timer related refs.
const startingTime = ref(Date.now());
const timeElapsed = ref(0);
const displayTimeElapsed = ref(false);

// AXIOS INSTANCE
const axiosInstance = axios.create({
  baseURL: "",
})

// Set axios interceptors
axiosInstance.interceptors.response.use(async (response: AxiosResponse) => {
  if (response.status == 202) {
    // This should only return if we are conducting polling.
    console.log("HTTP 202 received, polling the operation...");

    console.log(response.data);

    const task_id: number = response.data.id;
    const task_location: string = response.data.location;
    console.log("Operation task id: " + task_id);
    console.log("Operation location: " + task_location);

    // Retrieve the initial operation status
    console.log("Polling now for a response...")
    let pollingResponse = await axios.get("/backend" + task_location);
    console.log("Operation status is " + pollingResponse.data.status);

    // Helper function to make a looping timer.
    function timer(ms: number) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }

    // Loop until we get either positive or negative response.
    // In reality, there should be some sort of timeout here as well.
    while (pollingResponse.data.status != "SUCCESS" && pollingResponse.data.status != "FAILURE") {
      console.log("Fetching a new status...")
      await timer(3000);
      pollingResponse = await axios.get("/backend" + task_location);
      console.log("Operation status is " + pollingResponse.data.status);
    }

    if (pollingResponse.data.status === "FAILURE") {
      throw "Operation failed!";
    }
    
    console.log("Operation succeeded! Task is now ready for download.");

    console.log("Attempting to download the file...");
    try {
      const downloadResponse = await axios.get(
        "/backend/downloads/" + pollingResponse.data.result,
        { 
          responseType: "blob" 
        }
      );
      console.log("Download success! Downloading the file...")
      return downloadResponse
    }
    catch (e) {
      console.log(e);
      throw "Error, file could not be downloaded."
    }
  }
  // If not a 202 response return as normal.
  console.log("This is normal response." + response.status);
  return response;
}, (error) => {
  return Promise.reject(error);
}
);

// UPLOADING A FILE //
const { files, open, reset } = useFileDialog();
const uploadFile = async (url: string, worker=false) => {
  if (files.value == null) return
  if (files.value.length <= 0) return
  
  // Start a timer.
  startingTime.value = Date.now();

  let formData = new FormData();
  formData.append("file", files.value[0]);
  reset();

  const axiosConfig: RawAxiosRequestConfig = {
    headers: {
        "Content-Type": "multipart/form-data"
    },
    responseType: "json"
  }
  // If the upload type is not a worker, 
  // change the axios request config.
  if (worker != true) {
    axiosConfig.responseType = "blob"
  }
  try {
    // Make a request and download the response.
    loading.value = true;
    const response = await axiosInstance.post(url, formData, axiosConfig);
    console.log("Starting the download...")
    // Axios response doesn't initiate download on its own.
    // We can use a library to do it automatically for us.
    // We could also save the response to a value that could
    // be downloaded from a link click.
    FileDownload(response.data, "new_file.xlsx");
    console.log("Download ready!")
    loading.value = false;
    reset();

    // Calculate the elapsed time since the file upload and
    // make the elapsed time value visible.
    timeElapsed.value = Date.now() - startingTime.value;
    displayTimeElapsed.value = true;
  }
  catch(e) {
    loading.value = false;
    console.log(e);
  }
};
</script>

<template>
  <div class="container">
    <div v-if="loading">
      <div class="loader"></div>
      <p>Uploading...</p>
    </div>
    <div v-else>
      <div class="buttons">
        <button type="button" @click="open()">Select File</button>
        <button 
          type="button" 
          style="background-color:slategray"
          @click="uploadFile(url)"
        >
          Upload
        </button>
        <button
          type="button"
          style="background-color:aliceblue;color:rgb(17, 35, 52)"
          @click="uploadFile(pollingUrl, true)"
        >
          Worker Upload
        </button>
        <button
          type="button"
          style="background-color:lightcoral;"
          @click="reset()"
        >
          Clear
        </button>
      </div>
    </div>
    <div class="file-info">
      <p v-show="displayTimeElapsed">Last upload duration: {{ timeElapsed / 1000 }} seconds</p>
      <p v-for="file in files" :key="(file as File).name" class="file-info">
          Name: {{ (file as File).name }} <br>
          Type: {{ (file as File).type }} <br>
          Size: {{ (file as File).size / 1000000 }} mb
      </p>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  gap: 5em;
}
.file-info {
  width: 14em;
}
.loader {
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-info {
  text-align: start;
}

@media only screen and (max-width: 768px) {
  .container {
    flex-direction: column;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>