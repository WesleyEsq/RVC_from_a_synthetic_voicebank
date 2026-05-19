import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import zipfile
from pathlib import Path

def process_voicebank():
    # Prompt user for the target folder
    source_dir = filedialog.askdirectory(title="Select Voicebank Folder")
    if not source_dir:
        return

    source_path = Path(source_dir)
    dataset_dir = Path("dataset")
    output_zip = Path("dataset.zip")

    try:
        # Prepare a clean staging directory
        if dataset_dir.exists():
            shutil.rmtree(dataset_dir)
        dataset_dir.mkdir(exist_ok=True)

        status_label.config(text="Status: Scanning and extracting .wav files...")
        root.update()

        # Find all .wav files recursively
        wav_files = list(source_path.rglob("*.wav"))
        if not wav_files:
            messagebox.showwarning("No Files", "No .wav files found in the selected directory.")
            status_label.config(text="Status: Idle")
            return

        # Copy and flatten into the dataset directory, renaming to avoid collisions
        for i, wav_file in enumerate(wav_files):
            new_name = f"{i:04d}_{wav_file.name}"
            shutil.copy2(wav_file, dataset_dir / new_name)

        status_label.config(text="Status: Zipping dataset for Google Drive...")
        root.update()

        # Create the zip archive
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in dataset_dir.glob("*.wav"):
                zipf.write(file, file.name)

        # Cleanup the unzipped staging folder to save space
        shutil.rmtree(dataset_dir)

        status_label.config(text="Status: Done! dataset.zip is ready.")
        messagebox.showinfo("Success", f"Successfully extracted {len(wav_files)} files.\nArchived to: {output_zip.absolute()}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        status_label.config(text="Status: Error")

# --- GUI Setup ---
# Yeah this is a bit overkill but sure
root = tk.Tk()
root.title("Adachi Rei RVC: Dataset Preparer")
root.geometry("400x200")
root.resizable(False, False)

instruction = tk.Label(root, text="Select the raw UTAU voicebank folder.\nThe tool will extract all .wavs and create a zip for Drive.", justify="center")
instruction.pack(pady=15)

btn = tk.Button(root, text="Select Folder & Process", command=process_voicebank, width=25, height=2)
btn.pack()

status_label = tk.Label(root, text="Status: Not used yet", fg="gray")
status_label.pack(side="bottom", pady=10)

root.mainloop()