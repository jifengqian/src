from __future__ import division
import os
import time
import datetime
#step 1: Test if both two folders exist and the total number of folder is the same
#step 2: Test if the total number of files is the same.
#step 3: Test if the difference of the filesize beyone tolerance
#setp 4: Test if the content in the index.html is the identical or in tolerance range. 
#step 5: Test the differential expression results
import DicComp
import Configurations_param
import PicComp
import MetricsComp
import filecmp

def getallfilenum(path):
    num=0
    for files in os.walk(path):
        for name in files:
            num=num+1  # count how many files found so far
    return num

def getfullname_parent(path,filename,parentname): # get filename under the parentname folder in path
    targetfile=[]
    for r, d, f in os.walk(path):
        for files in f:
            #print files, filename,files.endswith(filename), r, parentname, r.endswith(parentname)
            if files.endswith(filename) and r.endswith(parentname): # if this is the target file under specific folder, then extract the path
                targetfile.append(os.path.join(r,files))
    return targetfile


def getfullname(path,filename): #search every files in that path, including the sub folders, to get the filename
    targetfile=[]      
    for r,d,f in os.walk(path): #search everything in the path, including the sub folder. 
        for file in f:
            if file.endswith(filename): # if the founded filename is the same as the input filename
                #print file, filename, file.endswith(filename),cmp(filename,file)
                if os.path.isfile(os.path.join(r,file)):
                    targetfile.append(os.path.join(r,file)) # if this is a file instead of symbolink or something else
    return targetfile

def getfullname_igncase(path,filename): #search every files in that path, including the sub folders, to get the filename
    targetfile=[]
    for r, d, f  in os.walk(path): #search everything in the path, including the sub folder.
        print r, d, f
        for file in f:
            filelower=file.lower()
            #if files.endswith("Genes.json"): 
            if filelower.endswith(filename): # if the founded filename is the same as the input filename
                #print file, filename, file.endswith(filename),cmp(filename,file)
                targetfile.append(os.path.join(r,file))
    return targetfile

def getextension(path,ext): #search every files in that path, including the sub folders, to get the filename
    targetfile=[]
    for r,d,f in os.walk(path): #search everything in the path, including the sub folder. 
        for files in f:
            if files.endswith(ext): # if the filename ends with the input extension
                targetfile.append(os.path.join(r,file))

def getfilename(path,ext): # search all the files in one specific folder, not including subfolder
    targetfile=[]
    filelist=os.listdir(path)
    for filename in filelist:
        if filename.endswith(ext):
            targetfile.append(filename)
    return targetfile

def csvchecking(bpath,npath):
    bcsv=getfullname_igncase(bpath,'.csv')
    errornum=0
    errormsg=''
    blen=len(bpath)
    for fullpath in bcsv:
        csvclass=MetricsComp.ClassifyMetrics(fullpath)
        partpath=fullpath[blen:]
        if csvclass==1:
            [errornum1, errormsg1]=MetricsComp.CompMetricsCsv_3column(fullpath,os.path.join(npath,partpath.lstrip("\\").lstrip("\/")),0.05)
            errornum=errornum+errornum1
            errormsg=errormsg+errormsg1
        elif csvclass==0:
            if not filecmp.cmp(fullpath,os.path.join(npath,partpath.lstrip("\\").lstrip("\/"))): #check if the two files are exactly the same
                errornum=errornum+1
                errormsg=errormsg+'two sample sheets are not exactly the same'
        elif csvclass==2:
            [errornum3, errormsg3]=MetricsComp.CompMetricsCsv_2column(fullpath,os.path.join(npath,partpath.lstrip("\\").lstrip("\/")),0.05)
            errornum=errornum+errornum3
            errormsg=errormsg+errormsg3
    return [errornum, errormsg]

def indexchecking(bpath,npath):
#setp 4: Test if the content in the index.html is the identical or in tolerance range.
    #testcaseid=76691
    errornum=0
    errormsg=''
    bindexfile=os.path.join(os.path.join(bpath,os.path.join('Summary','Report')),'index.html')
    nindexfile=os.path.join(os.path.join(npath,os.path.join('Summary','Report')),'index.html')
    if os.path.isfile(bindexfile) and os.path.isfile(nindexfile):
        bdic=DicComp.ConvertHtmlToDic(bindexfile)
        ndic=DicComp.ConvertHtmlToDic(nindexfile)
        [errornum,errormsg]=DicComp.CompDic(bdic,ndic)
    else:
        errornum=1
        errormsg='index.html cannot be found!'
    return [errornum,errormsg]

def imagechecking(bpath,npath):
    errornum=0
    errormsg=''
    bimagefolder=os.path.join(os.path.join(bpath,os.path.join('Summary','Report')),'images')
    nimagefolder=os.path.join(os.path.join(npath,os.path.join('Summary','Report')),'images')
    imgtype=Configurations_param.imagetype
    if os.path.exists(bimagefolder) and os.path.exists(nimagefolder): # if both baseline and new folder are found. 
        imgnames=[]
        for i in imgtype:
            imgnames=imgnames+getfilename(bimagefolder,i)
        for i in imgnames:
            bimgfile=os.path.join(bimagefolder,i)
            nimgfile=os.path.join(nimagefolder,i)
            if os.path.exists(bimgfile) and os.path.exists(nimgfile):
                diff=PicComp.CompareImage(bimgfile,nimgfile)
                print "Checking image "+ bimgfile + nimgfile+', the histogram correlation is ' +str(diff)
                if diff < Configurations_param.imagecorrelation:
                    errornum=1
                    errormsg='these two images are too different'+bimgfile+' and '+nimgfile
                    return [errornum, errormsg]
            else:
                errornum=1
                errormsg='some image file are missing '+nimgfile+' or '+ bimgfile
                return [errornum,errormsg]
    else:
        errornum=1
        errormsg='some image folder are missing '+bimagefolder+ 'Or '+nimagefolder
        return [errornum,errormsg]
    return [errornum, errormsg]


def filechecking(bpath,npath):
#step 2: Test if the total number of files is the same.
#step 3: Test if the difference of the filesize beyone tolerance
    errornum=0
    errormsg=''
    #testcaseid=[76620,76313]
    if os.path.exists(bpath) and os.path.exists(npath): # if both baseline and new folder are found. 
        [bnum,bfileset, bfilesize]=getallfileNon0(bpath) # get all the file name and number of subfolder of the baseline
        [nnum,nfileset, nfilesize]=getallfileNon0(npath) # get all the file name and number of subfolder of the newresult
        print "there are "+str(bnum)+ " files in the baseline folder"+"and "+str(nnum)+" files in the test run folder"
        if bnum > nnum: # if there are more files in the baseline than the new folder
            extrafile=bfileset-nfileset
            extrafile_names=''
            for extrafile_names in extrafile:
                extrafile_names+=extrafile_names
            errornum=1
            errormsg='some file in the baseline can not been found in the new folder: '+extrafile_names
        elif bnum < nnum:# if there are more files in the baseline than the new folder
            extrafile =nfileset-bfileset
            extrafile_names=''
            for extrafile_names in extrafile:
                extrafile_names+=' '
                extrafile_names+=extrafile_names
            errornum=1
            errormsg='some new file is found in the new folder but not in the baseline folder '+extrafile_names
        else:
            for k in bfilesize.keys():
                print 'cheking filesize of ',k,"bsize=",bfilesize[k], "nsize=", nfilesize[k]
                if bfilesize[k]== 0:
                    if nfilesize[k] !=0:
                        errornum = 1
                        errormsg = k+'is empty in the baseline but have content in the newfile!'
                elif k.endswith('cluster'):
                    if abs(bfilesize[k]-nfilesize[k])/bfilesize[k]>Configurations_param.clusterfilesize_toler:
                        errornum=1
                        errormsg='the difference of size of '+k+'in the baseline files and new files are beyond our '+str(Configurations_param.clusterfilesize_toler)+' tolerance '                         
                elif abs(bfilesize[k]-nfilesize[k])/bfilesize[k]>Configurations_param.filesize_toler:
                    errornum=1
                    errormsg='the difference of size of '+k+'in the baseline files and new files are beyond our '+str(Configurations_param.filesize_toler)+' tolerance '
    else:
        errornum=1
        errormsg='Input baseline folder or new data folder can not be found'
    return [errornum, errormsg]


def folderchecking(bpath,npath):
#step 1: Test if both two folders exist and the total number of folder is the same
    errornum=0
    errormsg=''
    #testcaseid=76303
    if os.path.exists(bpath) and os.path.exists(npath): # if both baseline and new folder are found. 
        [bnum,bfolderset]=getallfolder(bpath) # get all the subfolder name and number of subfolder of the baseline
        [nnum,nfolderset]=getallfolder(npath) # get all the subfolder name and number of subfolder of the newresult
        print "there are "+str(bnum)+ " subfolder in the baseline folder"+"and "+str(nnum)+" subfolder in the test run folder"
        if bnum > nnum: # if there are more folder in the baseline than the new folder
            extrafolder=bfolderset-nfolderset
            extrafolder_names=''
            for extrafolder_name in extrafolder:
                extrafolder_names+=' '
                extrafolder_names+=extrafolder_name
            errornum=1
            errormsg='some folder in the baseline can not been found in the new folder: '+extrafolder_names
        elif bnum < nnum:# if there are more folder in the baseline than the new folder
            extrafolder =nfolderset-bfolderset
            extrafolder_names=''
            for extrafolder_name in extrafolder:
                extrafolder_names+=extrafolder_name
            errornum=1
            errormsg='some folder is found in the new folder but not in the baseline folder '+extrafolder_names
    else:
        errornum=1
        errormsg='Input baseline folder or new data folder can not be found'
    return [errornum, errormsg]


def getallfolder(path):
    num=0
    plen=len(path)
    folderset=set()
    for r, d, f in os.walk(path):
        for dname in d:
            ppath=r[plen:]
            folderset.add(ppath+dname)
            num=num+1
    return [num,folderset]

def check_pathlist(bpathlist,npathlist,prgramname,filename):
    filenum=len(bpathlist)
    msg=''
    if len(bpathlist) != len(npathlist):
        msg=prgramname+' error: number of '+filename+' files in baseline folder and newly generated folder are different!'
        return [filenum, msg]
    elif len(bpathlist) == 0:
        msg=prgramname+' warning: no '+filename+' files in baseline folder!'
        return [filenum, msg]
    return [filenum,msg]

def getallfile(path):
    num=0
    plen=len(path)
    fileset=set()
    filesize={}
    for r, d, f  in os.walk(path):
        for fname in f:
            ppath=r[plen:]
            fileset.add(ppath+fname)
            #print os.path.join(root, name)
            num=num+1
            filepath=os.path.join(r, fname)
            if os.path.islink(filepath): # if this file is just a soft link 
                filesize[fname]=1.0
            else:
                filesize[fname]=float(os.path.getsize(filepath))
    return [num,fileset,filesize]

def getallfileNon0(path): # Get all the files under the path with size not equal to 0
    num=0
    plen=len(path)
    fileset=set()
    filesizes={}
    for r, d, f  in os.walk(path):
        for fname in f:
            ppath=r[plen:] #this is just the filename itself    
            filepath=os.path.join(r, fname) #this is the filename with fullpath        
            if os.path.islink(filepath):
                filesize=1.0
            else:
                filesize=float(os.path.getsize(filepath)) # this is the filesize
            if filesize>0:
                num=num+1
                fileset.add(ppath+fname)
                filesizes[fname]=filesize #this is the filesize
    return [num,fileset,filesizes]

def writertestresult(processname,errornum, errormsg,testcaseid,testresultfolder):
    logfile=os.path.join(testresultfolder,'log.txt')
    resultfile=os.path.join(testresultfolder,'result.txt')
    #fr=open(resultfile,'a')
    #print >>fr, "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid

def namebytime(prename):
    time_sec = time.time()  
    currenttime=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time_sec))
    if type(prename) is str:
        return prename+currenttime

class Timeformat:
    def __init__(self, time_string="1970-1-1 00:00:00"):
        self.time_string = self._format_time_string(time_string)

    def _format_time_string(self, time_string):
        return time.strftime("%Y-%m-%d %H:%M:%S", self.get_struct(time_string))

    @property
    def time_struct(self):
        return self.get_struct(self.time_string)
    def get_struct(self, time_string):
        return time.localtime(self.get_seconds(time_string))

    @property
    def seconds(self):
        return self.get_seconds(self.time_string)
    def get_seconds(self, time_string):
        d = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")
        return time.mktime(d)

    def get_string(self, time_sec):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_sec))

    # time is 1970-01-01 08:00:00
    def check_diff_time(self, t1, t2):
        sec1 = int(self.get_seconds(t1))
        sec2 = int(self.get_seconds(t2))
        if sec1 > sec2:
            secdiff = sec1 - sec2
        else:
            secdiff = sec2 - sec1
            #print "time difference is", secdiff
        d = self.get_struct(self.get_string(secdiff))
        #print d
        day = d.tm_mday
        hour = d.tm_hour
        if d.tm_hour < 8:
            day -= 1
            hour = 24 + (d.tm_hour - 8)
        else:
            hour = d.tm_hour - 8

        return {
            "year"  :d.tm_year - 1970,
            "month" :d.tm_mon  - 1,
            "day"   : day - 1,
            "hour"  : hour,
            "min"   : d.tm_min,
            "sec"   : d.tm_sec,
        }        
if __name__ == "__main__":
    #files=folderchecking('C:\\Users\\jqian\\Desktop\\report2', 'C:\\Users\\jqian\\Desktop\\report2')
    #f=getfullname_parent('C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\2013-04-26_093340\\samples','fusion.out','tophat_main')
    #print f
    #csvchecking('C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-04-26_093340','C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-04-26_093340')
    print getfullname_parent('C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-07-29_134220','isoforms.fpkm_tracking','novel')
