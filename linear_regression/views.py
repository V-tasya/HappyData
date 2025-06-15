from django.shortcuts import render
import base64
import io
import numpy as np
import pandas as pd
from uploading_and_processing_file.models import UploadedFile
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def linear_regression(request):
    if request.method == 'POST' and 'predict_button' in request.POST:
        target_column = request.POST.get('target_column', '').strip()
        file_id = request.session.get('uploaded_file_id')
        up_file = UploadedFile.objects.get(id=file_id)
        data_frame = pd.read_csv(up_file.file.path)
        
        if not target_column:
            return render(request, 'analysis_page.html', {'regression_error': 'Please enter target column name.'})
            
        if target_column not in data_frame.columns:
            return render(request, 'analysis_page.html',{'regression_error': 'Target column was not found'})
        
        if not pd.api.types.is_numeric_dtype(data_frame[target_column]):
            return render(request, 'analysis_page.html',{'regression_error': 'Target column should contain numerical values'})
        
        data_frame[target_column] = data_frame[target_column].fillna(0)
            
        try:
            data_frame = pd.get_dummies(data_frame, columns=data_frame.select_dtypes(include=['object']).columns)
            
            for column in data_frame.columns:
                if column != target_column and pd.api.types.is_numeric_dtype(data_frame[column]):
                    data_frame[column] = data_frame[column].fillna(data_frame[column].median())
            
            if target_column not in data_frame.columns:
                return render(request, 'analysis_page.html', {'regression_error': 'Target column was lost during preprocessing'})

            X = data_frame.drop(columns=[target_column])
            y = data_frame[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            plt.figure(figsize=(6, 4))
            
            sorted_indices = y_test.argsort()
            y_test_sorted = y_test.iloc[sorted_indices]
            y_pred_sorted = y_pred[sorted_indices]
            
            plt.plot(y_test_sorted.values, label='Actual Values', color='blue', alpha=0.7)
            plt.plot(y_pred_sorted, label='Predicted Values', color='red', alpha=0.7)
            
            plt.title('Actual vs Predicted Values')
            plt.xlabel('Sample Index')
            plt.ylabel(target_column)
            plt.legend()
            plt.grid(True)
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            regression_graph_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()
            
            return render(request, 'analysis_page.html',{
                'mae': round(mae, 2),
                'rmse': round(rmse, 2),
                'regression_graph_base64': regression_graph_base64
            })
            
        except Exception as e:
            return render(request, 'analysis_page.html',{'regression_error': f'Error in regression {e}.'})
    
    return render(request, 'analysis_page.html',{})