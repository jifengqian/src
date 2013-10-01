'''
Created on May 17, 2013
This is for check if the index.html are the same or little variation between the baseline and new job output
@author: jqian
'''

import Html2dic
import Configurations_param
def ConvertHtmlToDic(input_html): # convert an html file to a dictionary, using the table name as the key and table content as value
    parser = Html2dic.JFHTMLParser()
    f = open(input_html)
    data=f.read()
    f.close()
    parser.feed(data)
    return parser.dic_table

def CompDic(dic_baseline,dic_new): #Compare if the difference of the two dictionary are tolerable
    errornum =0
    errormsg ='' 
    if len(dic_baseline)!= len(dic_new): 
        errornum=1
        errormsg='number of table in the baseline folder and new run folder is not the same'
    else:
        for tablename in dic_baseline.keys():
            print "checking tablename:", tablename
            if tablename == 'Read Summary':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1,2],table_baseline,table_new)+CheckSumVariable([3,4,5,6,7],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Alignment Summary':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1,2,3],table_baseline,table_new)+CheckSumVariable([4,5,6],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Aligned Reads Detail':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1,2],table_baseline,table_new)+CheckSumVariable([3,4,5,6,7],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Abundant Reads Detail':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1,2],table_baseline,table_new)+CheckSumVariable([3,4,5,6,7],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Inserts Detail':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1],table_baseline,table_new)+CheckSumVariable([2,3,4],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Coverage Detail':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1,2],table_baseline,table_new)+CheckSumVariable([3,4,5,6,7,8,9,10],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Fusion Calls':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1],table_baseline,table_new)+CheckSumVariable([2],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Novel Assemblies':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0],table_baseline,table_new)+CheckSumVariable([1,2,3,4,5,6,7,8],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            elif tablename =='Differential Expression':
                table_baseline=dic_baseline[tablename]
                table_new=dic_new[tablename]
                errornum=CheckSumIdentity([0,1],table_baseline,table_new)+CheckSumVariable([2,3,4,5],table_baseline,table_new,Configurations_param.table_content_toler)
                if errornum>0:
                    errormsg = tablename+' metrics do not match to baseline.'
            else:
                errornum=1
                errormsg='do not understand this table name:'+tablename
    return [errornum,errormsg]


def CheckSumIdentity(col,btable,ntable): # checking if the colth column of the two table are identical
    numinequal=0
    if btable.shape!=ntable.shape:
        numinequal=1
        return numinequal
    else:
        if btable.ndim >1: # if there is only one row in the two tables
            for i in range(btable.shape[0]): # the row number
                for j in col: # the column number
                    numinequal=numinequal+CheckIdentity(i,j,btable,ntable)
            return numinequal
        else:
            for j in col:# the column number
                numinequal=numinequal+CheckIdentity('n',j,btable,ntable)
            return numinequal

def CheckSumVariable(col,btable,ntable,perct): # check if the difference of the colth column are tolerable
    numinequal=0
    if btable.shape!=ntable.shape:
        numinequal=1
        return numinequal
    else:
        if btable.ndim >1: # if there is only one row in the two tables
            for i in range(btable.shape[0]): # the row number
                for j in col: # the column number
                    numinequal=numinequal+CheckVariable(i,j,btable,ntable,perct)
            return numinequal
        else:
            for j in col: # the column number
                numinequal= numinequal+CheckVariable('n',j,btable,ntable,perct)
            return numinequal

    
def CheckIdentity (num_row, num_col,btable,ntable): # check if the two elements on the specific position of the two tables are identical
    if num_row=='n': # if these table are one dimension tables
        if btable[num_col]==ntable[num_col]:
            return 0
        else:
            return 1
    else:
        if btable[num_row][num_col]==ntable[num_row][num_col]:
            return 0
        else:
            return 1

def CheckVariable (num_row, num_col,btable,ntable,perct): # check if the difference of the cells in the two tables are in the tolerable range
    if num_row=='n': # if these tables are one dimension tables
        bdata=Str2numFormat(btable[num_col])
        ndata=Str2numFormat(ntable[num_col])
        if bdata !=0: # if the baseline content is not 0
            if abs(bdata-ndata)/bdata<perct: # if the difference is in a tolerate range
                return 0
            else:
                return 1
        else:
            if ndata ==0:
                return 0
            else:
                return 1
    else:
        bdata=Str2numFormat(btable[num_row][num_col])
        ndata=Str2numFormat(ntable[num_row][num_col])
        if bdata !=0:  # if the baseline content is not 0
            if abs(bdata-ndata)/bdata<perct: # if the difference is in a tolerate range
                return 0
            else:
                return 1
        else:
            if ndata ==0:
                return 0
            else:
                return 1
            
def Str2numFormat(str): # change the string content into float
    str=str.replace(',','')
    if str.startswith('nan'):
        return 0
    elif str.endswith('%'):
        return float(str.split('%')[0])*0.01
    elif str.endswith('x'):
        return float(str.split('x')[0])
    else:
        return float(str)
    
if __name__ == "__main__":
    dic_table=ConvertHtmlToDic('index.html')
    #print dic_table
    [errornum,errormsg]=CompDic(dic_table,dic_table)
    print errornum, errormsg
