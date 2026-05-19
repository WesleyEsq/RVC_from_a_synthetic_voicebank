import { pthToOnnx } from 'rvc-onnx-web';
import { readFileSync, writeFileSync } from 'fs';

const inputPath = process.argv[2];
const outputPath = process.argv[3];

async function convert() {
    try {
        console.log(`Reading ${inputPath}...`);
        const pthBuffer = readFileSync(inputPath);
        
        console.log("Converting to ONNX... (This may take a moment)");
        const { onnxBuffer, sampleRate, checkpoint } = await pthToOnnx(pthBuffer, { opsetVersion: 17 });
        
        console.log(`Conversion successful!`);
        console.log(`Sample Rate: ${sampleRate}Hz`);
        console.log(`Weights mapped: ${checkpoint.weights.size}`);
        
        writeFileSync(outputPath, Buffer.from(onnxBuffer));
        console.log(`Saved to ${outputPath}`);
    } catch (error) {
        console.error("Error during conversion:", error);
    }
}

convert();