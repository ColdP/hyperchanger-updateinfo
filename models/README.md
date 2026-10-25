# 空间壁纸实验室：抠图模型

原有 `u2netp.onnx` 保留，旧用户默认仍使用它。新增两种可选模型，在实验室的「抠图模型」下拉菜单切换，分别下载，不会互相替换。

| 模型文件 | 大小（bytes） | 输入 | 用途 |
| --- | ---: | --- | --- |
| u2netp.onnx | 4,574,861 | RGB float32 NCHW，320×320 | 原有轻量模型，快速预览 |
| isnet-general-int8.onnx | 44,229,662 | RGB float32 NCHW，1024×1024 | 均衡选择，建议优先尝试 |
| birefnet-lite-int8.onnx | 90,764,431 | RGB float32 NCHW，1024×1024 | 复杂轮廓、细节，耗时和内存较高 |

INT8 在这里表示权重量化；激活仍为 float32，运行内存不会等比例降到四分之一。

## 来源与许可

- ISNet：[xrds/isnet-general-onnx-int8](https://huggingface.co/xrds/isnet-general-onnx-int8/tree/71eff2372ec9c8edbc6ca637ded591423d23b65a)。固定 revision `71eff2372ec9c8edbc6ca637ded591423d23b65a` 的 `onnx/model_quantized.onnx`，仅重命名为 `isnet-general-int8.onnx`。模型卡和附带 LICENSE 标注 MIT，原始导出来源 [imgly/isnet-general-onnx](https://huggingface.co/imgly/isnet-general-onnx)。许可见 `LICENSE-ISNet.txt`。
- BiRefNet Lite：[官方项目](https://github.com/ZhengPeng7/BiRefNet)，[ONNX 导出](https://huggingface.co/onnx-community/BiRefNet_lite-ONNX/tree/de15b22ba131738a16dff04aab8bdf8dc32e3ac1)。固定 revision `de15b22ba131738a16dff04aab8bdf8dc32e3ac1` 的 `onnx/model.onnx`，原始 SHA-256 `5600024376f572a557870a5eb0afb1e5961636bef4e1e22132025467d0f03333`。使用本目录 `prepare_birefnet_lite.py` 将大权重做对称逐通道 INT8 + DequantizeLinear，保留 float32 运算，不依赖 ConvInteger 或额外 NDK 编译。模型卡及官方仓库标注 MIT，许可见 `LICENSE-BiRefNet.txt`。

这些是通用前景分割模型，不能保证所有照片和立绘都有相同效果。未采用 RMBG 2.0，因体积大且有非商用许可限制。

## 校验

```text
309c8469258dda742793dce0ebea8e6dd393174f89934733ecc8b14c76f4ddd8  u2netp.onnx
3b21a6706dc8d6e4ba9f5b31ebc6940f6c785b58862e27bb25daa9dd4424b87f  isnet-general-int8.onnx
2cffd9a8441691513a3d1d0990b5b154796f2351ba5ecb22f8ff802ac9dba1d1  birefnet-lite-int8.onnx
```

## 推理约定

- 保持 RGB 通道，直接缩放到表格尺寸，float32 NCHW。
- U2Netp：沿用应用原来的 ImageNet 归一化，`(RGB/255 - [0.485,0.456,0.406])/[0.229,0.224,0.225]`；取第一个输出，沿用原来的连通域清理及模糊。
- ISNet：`(RGB - 128)/256`，不要先除 255；取第一个输出，模型已包含 Sigmoid，不再应用 Sigmoid。
- BiRefNet Lite：ImageNet 归一化，同 U2Netp；取第一个输出（logits），先应用 Sigmoid。
- 三者输出均为 `[1,1,H,W]`，执行 min-max 归一化，再缩放到原图比例。新模型保留连续蒙版，避免二值化破坏发丝、柔和边缘和分离的小主体。
- 有透明通道的图片仍优先使用 Alpha；关闭「使用抠图模型」后沿用深度派生蒙版。

## 已做的验证（2026-10-25）

三个文件均通过大小、SHA-256、ONNX checker 和 ONNX Runtime 1.31.0 CPU 真实图片推理检查。输入测试图片来自 [rembg examples/girl-1.jpg](https://github.com/danielgatis/rembg/blob/main/examples/girl-1.jpg)。

Windows CPU / 4 线程，单张示例推理约：U2Netp 0.19 秒，ISNet 1.39 秒，BiRefNet Lite INT8 11.08 秒；不包含模型加载。此结果不能作为手机耗时承诺。

同一张图片上，BiRefNet INT8 与原始 FP32 的归一化蒙版平均绝对误差约 0.0000964，阈值 0.5 的 IoU 约 0.99946。该检查用于发现量化故障，不是完整数据集精度评测。尚未在 Android 真机验证耗时、峰值内存和视觉效果。

## 发布

将新增 ONNX、两个 LICENSE、本说明和量化脚本一并通过 Git 提交至仓库 `main`。两个新模型都小于普通 Git 单文件 100 MiB 限制；无需 Git LFS。网页上传的 25 MB 限制不适用于 Git push。

GitHub Pages 发布完成后，应用将从以下固定地址下载并校验：

- https://coldp.github.io/hyperchanger-updateinfo/models/isnet-general-int8.onnx
- https://coldp.github.io/hyperchanger-updateinfo/models/birefnet-lite-int8.onnx

不需要修改应用更新用的 `update.json`。保留原来的 `u2netp.onnx` 和其他深度模型。
