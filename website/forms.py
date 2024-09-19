from django import forms

class UploadFileForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')