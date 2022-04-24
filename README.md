TODO:
- Proper settings window
- Better styling for system tray menu and snippnig popup
- Hide snipping popup in taskbar

<h2 align="center">Manga2OCR</h2>

<p align="center"> [WIP] Snipping utility for the MangaOCR model </p>

## Contents
- [About](#about)
- [User Guide](#user_guide)
- [Installation](#installation)
- [Acknowledgments](#acknowledgements)
</br></br>

## About <a name = "about"></a>
Manga2OCR is a snipping tool for the [Manga OCR library](https://pypi.org/project/manga-ocr/). The project works similarly to [Capture2Text](http://capture2text.sourceforge.net/) but uses the MangaOCR model instead. See demo below to see how it works.

https://user-images.githubusercontent.com/45705751/161961152-29070fde-03f6-42a7-8569-0ff22ae9b014.mp4

## User Guide  <a name="user_guide"></a>
Follow the installation instructions [here](#installation). Launch the application, wait for the model to load, and start performing OCR using the shortcut `Alt+Q` 

## Installation <a name = "installation"></a>
[NOT RELEASED YET] Download the latest zip file [here](https://github.com/bluaxees/Manga2OCR/releases/latest/). Decompress the file in the desired directory. Make sure that the `app` folder is in the same folder as the shortcut `Manga2OCR`.

For developers, clone this repo and install requirements: `pip install -r requirements.txt`. Run the app in the command line using `python main.py`. 

### System Requirements

Recommended:
- Hard drive: at least 800 MB HD space
- RAM: at least 2 GB (recommended)

For developers, the following Python versions are supported: 3.7, 3.8, and 3.9.

## Acknowledgements <a name = "acknowledgements"></a>
This project will not be possible without the MangaOCR model by [Maciej Budyś](https://github.com/kha-white).

The software is licensed under GPLv3 (see [LICENSE](LICENSE.md)) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY.md)).

The icons used in this project are from [Icons8](https://icons8.com).
