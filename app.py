from flask import Flask, request, jsonify, render_template
import PyPDF2
from generate_gpt_text import gen_gpt_output

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
        generated_text = gen_gpt_output(pdf_text)

        # Return the generated text
        return jsonify({'generated_text': generated_text})
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
