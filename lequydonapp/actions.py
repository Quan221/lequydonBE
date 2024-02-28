import csv
from django.http import HttpResponse
from .models import DonTuyenSinh
import xlwt

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mymodel.csv"'

    writer = csv.writer(response)
    field_names = [field.name for field in DonTuyenSinh._meta.fields]
    writer.writerow(field_names)

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response
export_as_csv.short_description = "Export selected objects to CSV"

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mymodel.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('MyModel')

    # Define the headers for the Excel file
    row_num = 0
    columns = [field.name for field in DonTuyenSinh._meta.fields]
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data rows to the Excel file
    for obj in queryset:
        row_num += 1
        row = []
        for field in obj._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                # write the string representation of the related object
                related_obj = getattr(obj, field.name)
                row.append(str(related_obj))
            else:
                # write the value of the field
                row.append(getattr(obj, field.name))
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response

export_to_excel.short_description = "Export to Excel"