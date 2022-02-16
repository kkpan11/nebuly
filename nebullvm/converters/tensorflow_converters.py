from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Union, Tuple, List

import tensorflow as tf
import tf2onnx.convert


def convert_tf_to_onnx(
    model: tf.Module,
    input_sizes: List[Tuple[int, ...]],
    output_file_path: Union[str, Path],
):
    """Convert TF models into ONNX.

    Args:
        model (tf.Module): TF model.
        input_sizes (List[tuple]): Sizes of the model's input tensors.
        output_file_path (Path): Path where storing the output file.
    """
    with TemporaryDirectory() as temp_dir:
        tf.saved_model.save(model, export_dir=temp_dir)
        inputs_str = " ".join(
            [
                f"input_{i}:0{list(input_size)}"
                for i, input_size in enumerate(input_sizes)
            ]
        )
        onnx_cmd = (
            f"python -m tf2onnx.convert --saved-model {temp_dir/'model.tf'} "
            f"--inputs {inputs_str} "
            f"--output {output_file_path} --opset 11"
        )
        subprocess.run(onnx_cmd)


def convert_keras_to_onnx(
    model: tf.keras.Model,
    input_sizes: List[Tuple[int, ...]],
    output_file_path: Union[str, Path],
):
    """Convert keras models into ONNX.

    Args:
        model (tf.Module): keras model.
        input_sizes (List[tuple]): Sizes of the model's input tensors.
        output_file_path (Path): Path where storing the output file.
    """
    spec = (
        tf.TensorSpec(input_size, tf.float32, name=f"input_{i}")
        for i, input_size in enumerate(input_sizes)
    )
    tf2onnx.convert.from_keras(
        model, input_signature=spec, opset=11, output_path=output_file_path
    )