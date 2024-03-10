from django.shortcuts import render
import PyPDF2
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            text = extract_text_from_pdf(pdf_file)
            summary = generate_summary(text)
            keywords = extract_keywords(text)
            return render(request, 'result.html', {'summary': summary, 'keywords': keywords})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def extract_text_from_pdf(pdf_file):
    with pdf_file.open('rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text


def generate_summary(text):
    # Split the text into sentences
    sentences = text.split('.')
    # Extract the first few sentences to form the summary
    summary = '. '.join(sentences[:3])  # You can adjust the number of sentences as needed
    return summary


def extract_keywords(text):
    # Split the text into words
    words = text.split()
    # Extract the first few words as keywords
    keywords = ' '.join(words[:5])  # You can adjust the number of keywords as needed
    return keywords