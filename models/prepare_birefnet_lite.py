"""Create CPU-compatible weight-only INT8 BiRefNet Lite (activations remain float32).

Usage: python prepare_birefnet_lite.py SOURCE.onnx OUTPUT.onnx
Requires: onnx==1.23.2, numpy==2.5.4
Source: onnx-community/BiRefNet_lite-ONNX, revision
  de15b22ba131738a16dff04aab8bdf8dc32e3ac1/onnx/model.onnx
Source SHA256: 5600024376f572a557870a5eb0afb1e5961636bef4e1e22132025467d0f03333
Large float initializers are quantized with per-channel symmetric INT8. DequantizeLinear restores
float inputs for standard CPU operators; no ConvInteger or execution-provider-specific
operator is introduced.
"""
from pathlib import Path
import argparse
import hashlib
import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

SOURCE_SHA256 = "5600024376f572a557870a5eb0afb1e5961636bef4e1e22132025467d0f03333"

def convert(source, target):
    source, target = Path(source), Path(target)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256
    model = onnx.load(str(source))
    consumers = {}
    for node in model.graph.node:
        for index, name in enumerate(node.input):
            consumers.setdefault(name, []).append((node, index))
    initializers, dequantizers = [], []
    count = 0
    for weight in model.graph.initializer:
        users = consumers.get(weight.name, [])
        eligible = weight.data_type == TensorProto.FLOAT and len(weight.dims) >= 2
        eligible = eligible and np.prod(weight.dims) >= 2048 and users
        if not eligible:
            initializers.append(weight)
            continue
        values = numpy_helper.to_array(weight)
        # Exported Swin weights have Identity aliases as well as direct MatMul users.
        # Keep those aliases intact, restoring the exact original float tensor shape.
        direct = [(n, i) for n, i in users if n.op_type != "Identity"]
        axis = values.ndim - 1 if direct and all(n.op_type == "MatMul" and i == 1 for n, i in direct) else 0
        reduce_axes = tuple(i for i in range(values.ndim) if i != axis)
        scale = np.maximum(np.max(np.abs(values), axis=reduce_axes) / 127.0, 1e-8).astype(np.float32)
        shape = [1] * values.ndim
        shape[axis] = values.shape[axis]
        quantized = np.clip(np.rint(values / scale.reshape(shape)), -127, 127).astype(np.int8)
        prefix = weight.name + "_weight_int8"
        initializers.extend([
            numpy_helper.from_array(quantized, prefix),
            numpy_helper.from_array(scale, prefix + "_scale"),
            numpy_helper.from_array(np.zeros(scale.shape, dtype=np.int8), prefix + "_zero"),
        ])
        dequantizers.append(helper.make_node("DequantizeLinear", [prefix,prefix+"_scale",prefix+"_zero"], [weight.name], axis=axis, name=prefix+"_dequantize"))
        count += 1
    nodes = list(model.graph.node)
    del model.graph.node[:]
    model.graph.node.extend(dequantizers + nodes)
    del model.graph.initializer[:]
    model.graph.initializer.extend(initializers)
    metadata = model.metadata_props.add()
    metadata.key, metadata.value = "weight_quantization", "symmetric per-channel int8; float32 activations; source_sha256=" + SOURCE_SHA256
    onnx.checker.check_model(model)
    onnx.save(model, str(target))
    print(f"Quantized {count} weight tensors; {target.stat().st_size} bytes; SHA256 {hashlib.sha256(target.read_bytes()).hexdigest()}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    convert(args.source, args.target)
