# Japanese OCR model for HyperChanger Portal

- File: `jpn.traineddata`
- Model: Tesseract `tessdata_fast`, Japanese LSTM (`jpn`)
- Source: https://github.com/tesseract-ocr/tessdata_fast/blob/87416418657359cb625c412a48b6e1d6d41c29bd/jpn.traineddata
- Source revision: `87416418657359cb625c412a48b6e1d6d41c29bd`
- Size: 2,471,260 bytes
- SHA-256: `1f5de9236d2e85f5fdf4b3c500f2d4926f8d9449f28f5394472d9e8d83b91b4d`
- License: Apache-2.0; see `LICENSE-Tesseract.txt`. The upstream model is mirrored without modification.
- Pages download: https://coldp.github.io/hyperchanger-updateinfo/models/jpn.traineddata

HyperChanger downloads this file only when the user requests the Japanese OCR model. A partial download is verified before installation. Turning off the Portal Japanese OCR switch keeps the downloaded model; deleting it requires a separate confirmation.

This is an OCR text-recognition model, independent of the wallpaper depth/matting models. It does not change `update.json` or the application's release information. Recognition quality, especially small or vertical text, depends on the source image and needs device validation.
