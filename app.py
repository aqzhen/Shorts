from flask import Flask, request, jsonify, render_template, send_file
import PyPDF2
from generate_gpt_text import gen_gpt_output
from generate_movie import parse_generated_output, gen_scene_images, stitch_audio, overlay_images, stitch_movie
from generate_narration import text_to_voice, write_to_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file is a PDF
    if file.filename.endswith('.pdf'):
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(file)

        # Process text with GPT API (implementation required)
        print("Getting Mixtral Output")
        generated_text = str(gen_gpt_output(pdf_text))

        print(generated_text)

        # isolate scenes and narrations into lists
        narrations = parse_generated_output(generated_text + "}")

        print(narrations)

        # # generating scene images from extracted scene texts
        print("Generating images")
        gen_scene_images(narrations)

        # # generating Text to Speech narration from extraced narrations
        print("generating audio: ")
        for index, narration in enumerate(narrations):
            print(f"{index} out of {len(narrations)}")
            audio = text_to_voice(narration)
            write_to_file(audio, 'audio{}'.format(index))

        # # stitching audio clips together
        stitch_audio()

        # # overlay images on base video TODO: allow for changing of base video, movement of image to different spots
        overlay_images()

        # # stitch the entire move together
        stitch_movie("./audio/stitched_audio.mp3", "overlayed.mp4")

        # # Return the generated text
        return send_file('./result/output.mp4', mimetype='video/mp4')
    else:
        return jsonify({'error': 'Uploaded file is not a PDF'})


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text



if __name__ == '__main__':
    app.run(debug=True)
