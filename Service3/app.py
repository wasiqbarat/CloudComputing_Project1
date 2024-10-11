import schedule
import time
from Services import database_service
from Services import object_storage_service
from Services import text_to_image
from Services import mail_service
import io

def text_to_image_API(id, caption, email):
    image_bytes = text_to_image.call_api(caption)
    image_name = f"{id}_generated.jpg"

    #Uploade AI generated image to Storage server
    response = object_storage_service.upload_file(io.BytesIO(image_bytes), image_name)

    print(response)

    image_url = object_storage_service.generate_presigned_url(image_name)
    print(image_url)

    if response['message'] == "File uploaded successfully.":
        response1 = database_service.updateImageURL(id, image_url['message'])
        response2 = database_service.updateStatus(id, 'done')

        #Send email to the User
        mail_service.sendMail(id, email, image_url)
        
        print(response1, response2)
        return
    else:
        print("DB error")


def check_dB_requests_status():
    readyRequests = database_service.checkRequestsStatus()
    print(readyRequests)

    if readyRequests:
        id = readyRequests[0][0]
        caption = readyRequests[0][3]
        email = readyRequests[0][1]

        print(id, caption)
        print("before text to image")
        text_to_image_API(id, caption, email)
    return
    
schedule.every(3).seconds.do(check_dB_requests_status)

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()