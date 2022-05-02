<p align="center">
  <a href="" rel="noopener">
    <img width=100px height=100px src="doc/logo_doc.png" alt="Project logo">
  </a>
</p>
<h2 align="center">Cloe</h2>

<p align="center"> Snipping utility for the MangaOCR model </p>

## Contents
- [About](#about)
- [User Guide](#user_guide)
- [Acknowledgments](#acknowledgements)
</br></br>

## About <a name = "about"></a>
Inspired by [Capture2Text](http://capture2text.sourceforge.net/), Cloe is a snipping tool for the [Manga OCR library](https://pypi.org/project/manga-ocr/). The project works similarly to Capture2Text but uses the MangaOCR model instead. See demo below to see how it works.

https://user-images.githubusercontent.com/45705751/161961152-29070fde-03f6-42a7-8569-0ff22ae9b014.mp4

## User Guide  <a name="user_guide"></a>
Launch the application and wait for the model to load. Show the snipping window using shortcut `Alt+Q` and drag and hold the mouse cursor to start performing OCR.

### Installation <a name = "installation"></a>
Download the latest zip file [here](https://github.com/bluaxees/Cloe/releases/latest/). Decompress the file in the desired directory. Make sure that the `app` folder is in the same folder as the shortcut `Cloe`.

For developers, clone this repo and install requirements: `pip install -r requirements.txt`. Run the app in the command line using `python main.py`. 

### System Requirements

Recommended:
- Hard drive: at least 700 MB HD space
- RAM: at least 2 GB (recommended)

For developers, the following Python versions are supported: 3.7, 3.8, and 3.9.

## Acknowledgements <a name = "acknowledgements"></a>
This project will not be possible without the MangaOCR model by [Maciej Budyś](https://github.com/kha-white).

The software is licensed under GPLv3 (see [LICENSE](LICENSE.md)) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY.md)).

The icons used in this project are from [Icons8](https://icons8.com).
