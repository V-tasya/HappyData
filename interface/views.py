from django.shortcuts import render

def main_page(request):
  return render(request, 'main_page.html')

def analysis_page(request):
  return render(request, 'analysis_page.html')
