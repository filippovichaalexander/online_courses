from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicDocumentForm
from .models import TopicDocument

def document_list(request):
    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = TopicDocumentForm()

    documents = TopicDocument.objects.all()
    return render(request, 'document_list.html', {'form': form, 'documents': documents})

def update_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = TopicDocumentForm(instance=document)

    return render(request, 'update_document.html', {'form': form, 'document': document})

def delete_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        # delete file itself
        # if document.file:
        #     document.file.delete(save=False)
        # delete db row
        document.delete()
        return redirect('document_list')

    return render(request, 'confirm_delete.html', {'document': document})