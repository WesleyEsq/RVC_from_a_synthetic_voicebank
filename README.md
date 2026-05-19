# Adachi Rei RVC: Sidequest Project Overview

## The Problem

The goal is to deploy the **Adachi-HTTP** server, a C++ containerized text-to-speech pipeline that uses Piper for initial synthesis and RVC (Retrieval-based Voice Conversion) to match the synthetic timbre of an UTAU character named Adachi Rei, created by Missile39, as a non profit educational project.

However, there are several hurdles to overcome to get this software operational:

1. **Missing Weights:** The Adachi-HTTP repository provides the inference server code but does not distribute the required model weights due to licensing terms. You must independently source or train the RVC.
2. **Specific Acoustic Target:** Adachi Rei is an artificial voice. Preserving her robotic, synthetic tone requires strict dataset curation (raw `.wav` files only, no merged appends) and specific pitch extraction algorithms (RMVPE) during training to prevent smoothing out the mechanical artifacts.
3. **Format Requirement:** The Adachi-HTTP backend runs strictly on ONNX Runtime for CPU efficiency. Standard PyTorch (`.pth`) models exported by RVC will not work; the final model must be successfully compiled into `.onnx` format.
4. **Local Hardware and Dependency Constraints:** Training an RVC model locally on an RTX 2050 (4GB VRAM) is extremely slow and prone to Out-Of-Memory errors. Furthermore, older local RVC repositories suffer from severe dependency conflicts with modern Python 3.11 systems

---

## The Solution & Toolchain

To bypass local hardware limits and dependency hell, the project relies on a hybrid pipeline: local data preparation followed by cloud-based training using modernized tools.

### 1. Python (Local Data Extraction)

* **Purpose:** To isolate the clean audio data from the raw UTAU voicebank.
* **Usage:** A lightweight, dependency-free Python script (`extract_wavs.py`) utilizes the `pathlib` and `shutil` libraries to recursively scan the voicebank directory, extract only the raw `.wav` files recursively in the directory, and package them into a flat `dataset` folder, stripping away irrelevant engine caches (`.frq`, `.llsm`, etc.).

### 2. Google Colab (Cloud Hardware)

* **Purpose:** To provide the necessary computing power and a pre-configured environment.
* **Usage:** By uploading the zipped dataset to Google Drive and mounting it to a Colab notebook, you gain access to an Nvidia T4 GPU (15GB VRAM). This allows for less strain on local hardware at the cost of having the data on the cloud and dealing with the GCP.

### 3. Applio (RVC Framework)

**Purpose:** To preprocess the audio, extract features, train the model, and export it.

**Usage:** Applio is a fork of the RVC software that resolves the legacy Python conflicts. Operating within the Google Colab environment, Applio handles:
* **Preprocessing:** Slicing the `.wav` files and adjusting them to a 40kHz sample rate.
* **Feature Extraction:** Utilizing **RMVPE** (for highly accurate pitch tracking of the robotic voice) and **HuBERT** (for semantic feature extraction).
* **Training:** Processing the data over 150-200 epochs to establish the voice conversion matrix.

### 4. ONNX Exporter

* **Purpose:** To convert the trained PyTorch model into a format readable by the Adachi-HTTP C++ backend.
* **Usage:** Built directly into the Applio framework, the export function translates the final `.pth` weights into an `.onnx` graph. This file is then downloaded and placed in the `weights/` directory of your local Adachi-HTTP deployment to complete the pipeline.