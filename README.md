# OOPSE
Development of a vehicle identification system in automatic access control systems
System that detects license plates from images, recognise the text on the plates and if we have a match between text recognised and known set of license plates opens the gate.

Screenshots of outputs
![32aa1b9c-3fc9-4cab-bd2b-60020d043cc4](https://github.com/McSoo01/OOPSE/assets/170962578/d0af65cd-de3d-4f26-b314-9d10cfc96627)
Shows the phases of the image processing (whole image with the license plate detected, license plate cropped from the image and then license plate after converting to gray scale and setting a threshold.

![7d2c66c3-7934-4e45-9dbd-08a6afe2516c](https://github.com/McSoo01/OOPSE/assets/170962578/955a7d5c-038d-457c-8fbe-307af4017cfa)
At the beginning we get a notification whether the license plate we put in to be saved is already saved in the json file or not.

![9230be9e-396b-4c8e-95bc-965a1d6f9b37](https://github.com/McSoo01/OOPSE/assets/170962578/e296ad8c-fab0-4573-8160-1c1dfa09782a)
If we have a match the gate value will change to 1 (open).
Also we see that at the end we have an output about the gate status.
At the top of the screenshot we can see the outputs from the easyocr system (read license plate text and sureness of the recognition)

![aa2510ec-84f3-4e80-81eb-8e0f8225252d](https://github.com/McSoo01/OOPSE/assets/170962578/7b609a66-a1a0-4a01-a79f-9f6e2037192e)
If we did not found the match we will be asked to put in a set PIN to change the gate value to 1 (open), we have 3 tries to do so)

Conslusions:
The systems functionality was implemented successfully, although while trying to recognise a text using pictures that show license plates beyond certain angle or that are uneven lit the system has a problem in recognition. In such cases we can of course try to fine tune the image processing or change the values such as resolution of the
blobFromImage function, but it would be much better to use various images with the same license plate or a video. By using such method we can compare the outputs we get.
