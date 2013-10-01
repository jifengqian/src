'''
Created on Jun 6, 2013PIL support png

@author: jqian
'''
import PathJF
#import cv2
def CompareImage(image1, image2):
    hist1=getPolishedHist(image1)
    hist2=getPolishedHist(image2)
    distHist = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_CORREL)
    return distHist

def getPolishedHist(imgfilename):
    img = cv2.cvtColor(cv2.imread(imgfilename),cv2.cv.CV_RGB2GRAY)
    hist_item = cv2.calcHist([img],[0],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    return hist_item
    
if __name__ == "__main__":
    #c=PathJF.getfullname('C:\Users\jqian\Documents\My Box Files\RNA-SEQ\Data','HBR_HBR_100ng_35278_Aligned_QualityHistogram.png')
    #print "found",c
    im1 = get("C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-04-26_093340\\Summary\\Report\\images\\HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    #im2 = get("C:\Users\jqian\Documents\My Box Files\RNA-SEQ\Data\2013-04-26_093340\Summary\Report\images\UHR_UHR_100ng_35277_Aligned_QualityHistogram.png")
    #im3 = get("C:\Users\jqian\Documents\My Box Files\RNA-SEQ\Data\2013-04-26_093340\Summary\Report\images\HBR_HBR_100ng_35278_TranscriptCoverage.png")
    im1.shape
    #im2.shape
    #im3.shape