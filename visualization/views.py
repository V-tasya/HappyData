from django.shortcuts import render
from django.contrib import messages
from uploading_and_processing_file.models import UploadedFile
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
import csv
import io
import base64

def visualization_type(request):
    error = None
    image_base64 = None

    if request.method == "GET":
        return render(request, 'analysis_page.html', {'graph_image_base64': None})
    
    if request.method == "POST" and 'generate_button' in request.POST:
        file_id = request.session.get('uploaded_file_id')

        if not file_id:
            error = "You need to upload file first."
            return render(request, 'analysis_page.html', {'error_message': error})
        
        visualization_type = request.POST.get('select_plot') 
        col1 = request.POST.get('col1', '').strip()
        col2 = request.POST.get('col2', '').strip()

        try:
          up_file = UploadedFile.objects.get(id=file_id)
          data_frame = pd.read_csv(up_file.file.path)

          if visualization_type == 'heatmap':
            error, image = heatmap(data_frame)
          elif visualization_type =='boxplot':
            error, image = boxplot(data_frame, col1, col2)
          elif visualization_type == 'violinplot':
            error, image = violinplot(data_frame, col1, col2)
          elif visualization_type == 'hystogram':
            error, image = hystogram(data_frame, col1)
          elif visualization_type == 'scatterplot':
            error, image = scatterplot(data_frame, col1, col2)

          if image:  
            buf = io.BytesIO()
            image.savefig(buf, format='png', bbox_inches='tight', dpi=80)
            plt.close(image)
            buf.seek(0)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        except UploadedFile.DoesNotExist:
            error = "File not found. Upload it again."
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render(request, 'analysis_page.html', {
        'error_message': error,
        'graph_image_base64': image_base64
    })
    

def heatmap(data_frame):
  sns.set_style('whitegrid')
  numeric_columns = data_frame.select_dtypes(include=['number'])
  if numeric_columns.shape[1] == 0:
    return "This file does not contain numeric values", None
  
  fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
  sns.heatmap(numeric_columns.corr(), cmap='winter', annot=True, fmt='.2f', ax=ax)
  ax.set_title("Heatmap for numeric values")

  return None, fig

def boxplot(data_frame, col1, col2):
  if not col1 or not col2:
    return "You need to enter two values", None
  
  if col1 not in data_frame.columns or col2 not in data_frame.columns:
    return "One or bouth columns do not exist in the data base", None
  
  if col1 == col2:
    return "Columns should be different", None
  
  if not (pd.api.types.is_numeric_dtype(data_frame[col1]) or pd.api.types.is_numeric_dtype(data_frame[col2])):
    return "One of the columns should be numeric", None
  
  fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
  
  if pd.api.types.is_numeric_dtype(data_frame[col2]):
    sns.boxplot(x=col1, y=col2, data=data_frame, ax=ax)
  else:
    sns.boxplot(x=col2, y=col1, data=data_frame, ax=ax)

  ax.set_title(f"Boxplot")
  plt.xticks(rotation=45)
  return None, fig

def violinplot(data_frame, col1, col2):
  if not col1 or not col2:
    return "You need to enter two values.", None
  
  if col1 not in data_frame.columns or col2 not in data_frame.columns:
    return "One or bouth columns do not exist.", None
  
  if col1 == col2:
    return "Columns should be different.", None
  
  if not (pd.api.types.is_numeric_dtype(data_frame[col1]) or pd.api.types.is_numeric_dtype(data_frame[col2])):
    return "One of the columns should be numeric.", None
  
  fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
  
  if pd.api.types.is_numeric_dtype(data_frame[col2]):
    sns.violinplot(x=col1, y=col2, data=data_frame, ax=ax)
  else:
    sns.violinplot(x=col2, y=col1, data=data_frame, ax=ax)

  ax.set_title(f"Violinplot")
  plt.xticks(rotation=45)
  return None, fig

def hystogram(data_frame, col1):
  if not col1:
    return "You need to enter one value.", None
  
  if col1 not in data_frame.columns:
    return "Entered column does not exist.", None
  
  if not pd.api.types.is_numeric_dtype(data_frame[col1]):
    return "Entered column should be numeric.", None
  
  fig, ax = plt.subplots(figsize=(6,4), dpi=80)

  try:
    sns.histplot(data=data_frame, x=col1, kde=True, color='#4c72b0', edgecolor='white', linewidth=0.5, alpha=0.8, ax=ax)
    ax.set_title(f'Distribution of {col1}', pad=15, fontsize=14)
    ax.set_xlabel(col1, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True) 
    ax.ticklabel_format(style='plain', axis='x')
    plt.tight_layout()
        
  except Exception as e:
    plt.close(fig)
    return "Error occured while creating histogram.", None
    
  return None, fig

def scatterplot(data_frame, col1, col2):
  if not col1 or not col2:
    return "Please specify both columns.", None
    
  if col1 not in data_frame.columns or col2 not in data_frame.columns:
    return f"One or bouth columns do not exist.", None
    
  if col1 == col2:
    return "Please select different columns.", None

  if not (pd.api.types.is_numeric_dtype(data_frame[col1]) and pd.api.types.is_numeric_dtype(data_frame[col2])):
    return "Columns should contain numeric values.", None
    
  fig, ax = plt.subplots(figsize=(6, 4))
    
  try:
    sns.scatterplot(data=data_frame, x=col1, y=col2, color='#2b7bba', alpha=0.7, edgecolor='w', linewidth=0.3, s=60, ax=ax)
    sns.regplot(data=data_frame, x=col1, y=col2, scatter=False, color='#ff7f0e', line_kws={'linewidth': 2.5}, ax=ax)
    
    ax.set_title('Scatter Plot', pad=15, fontsize=14)
    ax.set_xlabel(col1, fontsize=12)
    ax.set_ylabel(col2, fontsize=12)
        
    ax.grid(alpha=0.3)
    ax.set_axisbelow(True)
    ax.ticklabel_format(style='plain')
    plt.tight_layout()
        
  except Exception as e:
    if 'fig' in locals():
      plt.close(fig)
    return "Error occurred while creating scatter plot.", None
    
  return None, fig