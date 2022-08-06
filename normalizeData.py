from locale import normalize
import openpyxl


oldData = openpyxl.load_workbook("D:/Programming/Repositories/screenerSettings/highVolume.xlsx", data_only=True) #data only ignores formula aspects 
normalizedData = openpyxl.load_workbook("D:/Programming/Repositories/irregularVolumeNN/normalizedData.xlsx")

oldDataWrite = oldData.worksheets[0]
normalizedDatawrite = normalizedData.worksheets[0]

#(value - 14631) / (209591899- 14631) for each data point, can flip if need to
#(v - min) / (max - min) for each unique column
def normalizeFloat(index):
    while(oldDataWrite.cell(column=4, row=index).value != None): #float
        normalizedDatawrite.cell(column=4, row=index).value = (oldDataWrite.cell(column=4, row=index).value - 14631) / (209591899- 14631)
        index += 1
        

def normalizeMktCap(index):
    while(oldDataWrite.cell(column=5, row=index).value != None): #float
        normalizedDatawrite.cell(column=5, row=index).value = (oldDataWrite.cell(column=5, row=index).value - 14631) / (209591899- 14631)
        index += 1

#(value - 0.01) / (150.08-0.01) for each data point, can flip if need to
#(v - min) / (max - min) for each unique column
def normalizePrice(index):
    while(oldDataWrite.cell(column=6, row=index).value != None): #float
        normalizedDatawrite.cell(column=6, row=index).value = (oldDataWrite.cell(column=6, row=index).value - 0.01) / (150.08-0.01)
        index += 1

#(value - (-0.8286) / (3.7577- (-0.8286)) for each data point, can flip if need to
#(v - min) / (max - min) for each unique column
def normalizeChange(index):
 
    while(oldDataWrite.cell(column=7, row=index).value != None): #float
        normalizedDatawrite.cell(column=7, row=index).value = (oldDataWrite.cell(column=7, row=index).value + 0.8286) / (3.7577 + 0.8286)
        index += 1

def expectedOutPut(index):
    while(oldDataWrite.cell(column=23, row=index).value != None): #float
        if(oldDataWrite.cell(column=23, row=index).value == "Green"):
            normalizedDatawrite.cell(column=10, row=index).value = 1
        else:
             normalizedDatawrite.cell(column=10, row=index).value = 0
        index += 1

# normalizeFloat(2)
# normalizeMktCap(2)
#normalizePrice(2)
#normalizeChange(2)
#expectedOutPut(2)

normalizedData.save("D:/Programming/Repositories/irregularVolumeNN/normalizedData.xlsx")