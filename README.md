
# RVC Trained with a Synthetic Voicebank

Linux-native scripts for preparing synthetic voicebank data locally and training Retrieval-based Voice Conversion (RVC) models in Google Colab. Windows users can run this through WSL.

Because of dependency hell and the fact that most consumer GPUs do not have enough VRAM to train RVC comfortably, this workflow splits the work: prepare the dataset on your own machine and then use Google Colab to train with the data. The sugested steps to follow are bellow.

## Included Tools

### 1. Dataset Preparer (`tools/extract_gui.py`)

A small Python GUI that recursively searches a directory for `.wav` files, copies them into a flat folder, and packages them into `dataset.zip`. It ignores engine caches, configuration files, and any non-audio data that usually clutter voicebank folders.

Run it with Python, point it at your voicebank root, and it will produce a clean archive ready for upload.

### 2. ONNX Converter (`tools/convert.sh`)

A Bash/Node.js wrapper around `rvc-onnx-web` that converts PyTorch `.pth` checkpoints to ONNX (opset 17). The script installs its own dependencies via `dnf` and `npm` if they are missing.

```bash
./tools/convert.sh <input_model.pth> <output_model.onnx>
```

## Recommended Workflow

**Step 1: Local Data Extraction**

Run `extract_gui.py` and select your voicebank folder. The tool will strip away everything except the raw `.wav` files and output `dataset.zip`.

**Step 2: Cloud Upload**

Upload `dataset.zip` to Google Drive so Colab can access it.

**Step 3: Model Training via Colab**

Use a premade RVC notebook (such as [Applio's](https://colab.research.google.com/github/iahispano/applio/blob/master/assets/Applio.ipynb)) and mount your Drive.

- Unzip the dataset into the Colab environment.
- Preprocess audio to 40 kHz.
- **Synthetic voices:** Use the **RMVPE** pitch extractor. It tracks robotic pitch artifacts more accurately than algorithms that smooth them out.
- Train for 150–200 epochs (90 can already give usable results).
- Set batch size to 40 to saturate a typical Colab GPU. Adjust down if you hit memory limits.

**Step 4: Download and Convert**

Download the resulting `.pth` from Colab. If you need CPU inference, convert it:

```bash
./tools/convert.sh my_trained_model.pth final_model.onnx
```

## Acknowledgments

Conversion is handled entirely by the `rvc-onnx-web` library, which parses the PyTorch weights and maps them into the correct ONNX graph.

---

## Results and observations from training the VCR

I personally used the voicebank of the UTAU character Adachi Rei as an example, and to use as a source for the training. She has a characteristic robotic voice to her that was achieved thanks to directly editing sine waves together on an audio editor. She was created by Missile 39 and you can see the rigths on how to use her character in [mechanicalgirl.jp](https://mechanicalgirl.jp/guidelines/) which allows educational projects and specially allows non profit activities such as this one. I do not have any personal aproval from her creator.

I specifically used the [Arpasing ENG](https://adachirei-eng.carrd.co/) voicebank because it had .wav sounds and so it was easier to work with. I probably should come back to make a version of this software that can produce sounds for training with Utau voicebanks but that is beyond the scope of this project.

### Google Colab and Applio

I first tried to make everything locally, by creating a ton of scripts that automatically installed and executed tools that ran on my own GPU and RAM, but I encountered some problems. Mainly, My GPU was underpowered for this task, because it had only 4GB VRAM. This meant I had to leave it running overnight and I didn't want to put my personal laptop into such stress.

So I found [this colab notebook](https://colab.research.google.com/github/iahispano/applio/blob/master/assets/Applio.ipynb) from applio that perfectly configured the entire enviroment for training in google colab, I copied it, and I used that and called it a day. 

By choosing the (currently as of 19 of may 2026) free T4 GPU instance, I executed the Applio and had to wait about two hours. Then I tried to export directly to onnx, which was the format that I needed, but could only find the option to directly download to pth.

### Finally, converting to the format I needed

If you need the pythorch extension then you would be done by now. But since I needed this other one, I had to keep going. I made this bash script and incorporated a javascript package for this exact task into this github. And that was the end of it.
