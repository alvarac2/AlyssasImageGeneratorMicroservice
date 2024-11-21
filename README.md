# AlyssasImageGeneratorMicroservice
A microservice that retrieves random images from wikimedia or the picture of the day

# Communication Contract
* Requesting Data
  * Write "random" or "picture_of_day" to the text file you are using to communicate
  * Example call:
    * with open(FILE_PATH, "w") as file:
        file.write("random")

* Receiving data
  * Read the text file to get the string URL of the image
  * Example call:
    * with open(FILE_PATH, "r") as file:
        return file.read().strip()

* UML Sequence Diagram
  * ![image](https://github.com/user-attachments/assets/ba3bfb9a-c41b-4bb6-9c9f-43728824bddc)
 
