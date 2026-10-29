# HyperChanger Portal multilingual OCR model

- Archive: `portal-ocr-eng-chi_sim-jpn.zip`
- Source: https://github.com/tesseract-ocr/tessdata_fast/tree/87416418657359cb625c412a48b6e1d6d41c29bd
- License: Apache-2.0; see `LICENSE-Tesseract.txt`. The upstream models are mirrored without modification.
- Archive size: 5,222,282 bytes
- Archive SHA-256: `cc6dc661ada9c96c8ddf3ee6e9a5a870ce409b4f5f94264392062571c8146b56`
- Pages download: https://coldp.github.io/hyperchanger-updateinfo/models/portal-ocr-eng-chi_sim-jpn.zip

| File | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| eng.traineddata | 4,113,088 | 7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2 |
| chi_sim.traineddata | 2,469,156 | a5fcb6f0db1e1d6d8522f39db4e848f05984669172e584e8d76b6b3141e1f730 |
| jpn.traineddata | 2,471,260 | 1f5de9236d2e85f5fdf4b3c500f2d4926f8d9449f28f5394472d9e8d83b91b4d |

HyperChanger downloads this archive only when the user requests it from the enhanced text recognition settings. The three language models are loaded together with Tesseract language selection `eng+chi_sim+jpn` for Chinese, Japanese, English, and mixed text. HyperChanger verifies the archive and each extracted model before installation.

The new application removes the previous Japanese-only model during startup, including any incomplete download. Disabling enhanced text recognition retains the new multilingual model; deletion requires separate confirmation. The old `jpn.traineddata` download remains available here for older application versions.

The archive is not included in the APK. It is independent of wallpaper depth/matting models and does not change `update.json` or release information. Download, integrity, extraction, cancellation, and migration have been checked; Android recognition accuracy and performance still require device validation.
