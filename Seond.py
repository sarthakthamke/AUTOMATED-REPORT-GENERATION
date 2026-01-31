import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def read_and_analyze_data(file_path):
    """
    Reads data from a CSV file and performs basic analysis.
    """
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        print(df.head())
        
        # Basic analysis
        total_sales = (df['Quantity'] * df['Price']).sum()
        average_price = df['Price'].mean()
        total_quantity = df['Quantity'].sum()
        product_counts = df['Product'].value_counts()
        
        analysis = {
            'total_sales': total_sales,
            'average_price': average_price,
            'total_quantity': total_quantity,
            'product_counts': product_counts,
            'data': df
        }
        
        return analysis
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def generate_pdf_report(analysis, output_file):
    """
    Generates a formatted PDF report using ReportLab.
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    story = []
    
    # Title
    story.append(Paragraph("Sales Data Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Summary section
    story.append(Paragraph("Summary Statistics", heading_style))
    story.append(Spacer(1, 12))
    
    summary_data = [
        ["Total Sales", f"${analysis['total_sales']:.2f}"],
        ["Average Price per Unit", f"${analysis['average_price']:.2f}"],
        ["Total Quantity Sold", str(analysis['total_quantity'])],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 24))
    
    # Product counts section
    story.append(Paragraph("Product Sales Breakdown", heading_style))
    story.append(Spacer(1, 12))
    
    product_data = [["Product", "Units Sold"]]
    for product, count in analysis['product_counts'].items():
        product_data.append([product, str(count)])
    
    product_table = Table(product_data, colWidths=[2*inch, 2*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(product_table)
    story.append(Spacer(1, 24))
    
    # Raw data section
    story.append(Paragraph("Raw Data", heading_style))
    story.append(Spacer(1, 12))
    
    # Convert DataFrame to list of lists for table
    data_list = [list(analysis['data'].columns)]
    for _, row in analysis['data'].iterrows():
        data_list.append(list(row))
    
    data_table = Table(data_list, colWidths=[1.2*inch, 1.5*inch, 1*inch, 1*inch])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(data_table)
    
    # Build the PDF
    doc.build(story)
    print(f"PDF report generated: {output_file}")

def main():
    """
    Main function to run the data analysis and PDF generation.
    """
    data_file = "sales_data.csv"
    output_pdf = "sales_report.pdf"
    
    analysis = read_and_analyze_data(data_file)
    
    if analysis:
        generate_pdf_report(analysis, output_pdf)
    else:
        print("Failed to analyze data.")

if __name__ == "__main__":
    main()
