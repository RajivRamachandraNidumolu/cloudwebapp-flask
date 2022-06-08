import os
from flask import Flask, request, redirect
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

connect_str = '######"

# create a blob service client to interact with the storage account
blob_service_client = BlobServiceClient.from_connection_string(
    conn_str=connect_str)
try:
    # get container client to interact with the container in which images will be stored
    container_client = blob_service_client.get_container_client(
        container=container_name)
    # get properties of the container to force exception to be thrown if container does not exist
    container_client.get_container_properties()
except Exception as e:
    print(e)
    print("Creating container...")
    # create a container in the storage account if it does not exist
    container_client = blob_service_client.create_container(container_name)


@app.route("/")
def view_photos():
    # list all the blobs in the container
    blob_items = container_client.list_blobs()
    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"
    for blob in blob_items:
        # get blob client to interact with the blob and get blob url
        blob_client = container_client.get_blob_client(blob=blob.name)
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/>".format(
            blob_client.url)  # get the blob url and append it to the html

    img_html += "</div>"
    # return the html with the images
    return """
    <head>
    
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">CloudADBApp</a>
            </div>
        </nav>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
            <h2 style="color:Red;text-align:Right;">Rajiv Ramachandra Nidumolu || UTA ID: 1001866606</h2>
                <h3>Upload a csv or image.</h3>
                
                <div class="form-group">
                    <form method="post" action="/upload-photos" 
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-control" style="margin-right: 1em;">
                            <input type="submit" class="btn btn-success">   
                        </div>
                    </form>
                    <div class="input-group">
  <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" />
  <button type="button" class="btn btn-info">search</button>
</div>
                </div> 
                
            </div>
        
    """ + img_html + "</div></body>"


@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""

    for file in request.files.getlist("photos"):
        try:
            # upload the file to the container using the filename as the blob name
            container_client.upload_blob(file.filename, file)
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames")  # ignore duplicate filenames

    return redirect('/')
