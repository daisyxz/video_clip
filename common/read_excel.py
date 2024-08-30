#coding=utf-8
import pandas as pd
from common import excel_data_mat

#20230906
def readExcelMatrix(file_path, sheet_name):  # all column
    print('read excel,path=' + file_path + ',sheet='+sheet_name)
    if sheet_name == "":
        df = pd.read_excel(io=file_path)
    else:
        df = pd.read_excel(io=file_path\
                       , sheet_name=sheet_name)
    header = df.columns
    attribte_idx_map = {header[i].strip():i for i in range(len(header))}
    if len(attribte_idx_map.keys()) < len(header):
        print('[ERROR] can read excel table with repeat column name: ' + file_path + '/sheet=' + sheet_name)
        return None
    #-------------- 将传入的df.values的numpy格式，转成二维list，便于后续使用
    data_mat = list()
    for line in df.values:
        new_line = list()
        for e in line:
            new_line.append(e)
        data_mat.append(new_line)
    #---------------20230920--------------------

    table = excel_data_mat.ExcelDataMat(attribte_idx_map, data_mat)
    return table

def readExcelMatrixDefaultSheet(file_path):  # all column
    print('read excel,path=' + file_path + ',defaul sheet')
    df = pd.read_excel(io=file_path)
    header = df.columns
    attribte_idx_map = {header[i].strip():i for i in range(len(header))}
    if len(attribte_idx_map.keys()) < len(header):
        print('[ERROR] can read excel table with repeat column name: ' + file_path + '/sheet=' + sheet_name)
        return None
    table = excel_data_mat.ExcelDataMat(attribte_idx_map, df.values)
    return table

def readExcelMatrixSubfield(file_path, sheet_name, fields):  # all column
    table = readExcelMatrix(file_path, sheet_name)
    data = table.submatByFileds(fields)
    attribte_idx_map = {fields[i].strip():i for i in range(len(fields))}
    table = excel_data_mat.ExcelDataMat(attribte_idx_map, data)
    return table

