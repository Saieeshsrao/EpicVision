
# Image Reconstruction and Facial Feature Extraction for Criminal Identification Using deep learning    -EpicVision






## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

## Run Locally

Clone the project

```bash
  git clone https://github.com/rakshikasprasad/EpicVision.git
```

Go to the FrontEnd

```bash
  cd FrontEnd
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Download the model files from the drive link below and place them in the FrontEnd folder

```bash
 https://drive.google.com/file/d/1ZLCd_HqniD1q5oXfNVmm7wkX-z6akjJ_/view
```
Replace the path to these pth files to your local  path after downloading in page2 ,page3, page4 files.

Now to set up the mail service you would need a api key and a secret key of your own which will help you to use the mail option,change these values in page4 file.

Also,you need to setup your sql database and change the db password in page4.

once all these setup is done simply run,

```bash
streamlit run main.py
```






## Demo

Insert gif or link to demo


## Screenshots
After converting video to frames
![App Screenshot](Outputs/before.jpg?raw=true)

Using RealESRGAN and GFPGAN models for enhancement
![App Screenshot](Outputs/after_gfp_and_realesr_GANs.jpg?raw=true)

Predictions of age gender race and emotion
![App Screenshot](Outputs/predictions.png?raw=true)



## Authors

- [@Saieesh S Rao](https://github.com/Saieeshsrao)
- [@Rakshika Prasad](https://github.com/rakshikasprasad)
- [@Nithanth Sawkar](https://github.com/NithanthSawkar)
- [@Shravya U](https://github.com/Shravya0408)
