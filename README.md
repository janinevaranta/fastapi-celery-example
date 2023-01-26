# FastAPI Celery Example

FastAPI and Celery example that showcases how the workflow between a backend API and worker service can be structured.
This example is made to work with Excel files (.xlsx). Using other file formats might cause an error or unexpected result.

## How does it work?

1. The example is launched by running the included docker-compose.yml file. To start, make sure you have Docker and docker compose installed and run the command `docker compose up -d --build`. This will also build the required containers.

2. Once the docker compose instance is up and running, you should be able to enter the frontend by navigating to the browser and entering the following URL: `frontend.localhost`.

3. The example includes a simple Vue frontend. Pressing the `Select File`-button should open a file dialogue window in your operating system. Choose an Excel (.xlsx) file.

4. Some information about the file should now be visible in the frontend, indicating the file was selected successfully. You can also press the `Clear`-button to clear the selected file and try again.

5. After selecting a file there are two options: either press the `Upload`-button or the `Worker Upload`-button. `Upload`-button will upload the file to the backend and it will be modified by the FastAPI itself, no workers involved. The `Worker Upload`-button on the other hand will initiate a Celery task and assign a worker to work on that task. After pressing either option the upload will begin and you can see a loader appear.

6. Depending on the button pressed and the size of the file you should receive a downloadable .xlsx file after a while. This file should now have been modified to have one additional sheet and some text in the first cell of the sheet.

7. The idea is to tinker around to see how the workers work and what's the difference between the two options. You can try uploading larger files and in separate frontend instance to see how each changing variable affects the processing time.

## How is it built?

The structure of the example is as follows:

* docker-compose
  * frontend
    * Built with Vite, Vue and Typescript.
    * Includes the additional libraries: axios, js-file-download and VueUse.
    * Runs on a simple Nginx server that redirects calls to backend to the backend .container
  * backend
    * Written in Python and FastAPI framework.
    * Utilizes openpyxl library for opening and modifying Excel files.
    * Runs on Uvicorn.
  * redis
    * Simple Redis image used as a broker database for the worker. Jobs awaiting handling and jobs that are ready both use the same broker.
  * worker
    * Runs on a copy of backend image but instead of initiating Uvicorn it runs the Celery app instance.
    * Tasks are defined in the backend folders worker.py script.
  * traefik
    * Traefik orchestrates the whole ordeal by acting as the reverse proxy entrance to the outside world. 
