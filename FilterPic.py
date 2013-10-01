'''
Created on Jun 7, 2013

@author: jqian
'''
from __future__ import division
from PIL import Image 
import numpy
import cv2
import scipy as sp
from scipy.misc import imread
def get(path): # get JPG image as Scipy array, RGB (3 layer)
    data = imread(path)  # convert to grey-scale using W3C luminance calc
    data = sp.inner(data, [299, 587, 114]) / 1000.0    # normalize per http://en.wikipedia.org/wiki/Cross-correlation, get the luminance value
    return (data - data.mean()) / data.std()

def rgb2cmyk (rgb) :
    r,g,b=rgb
    c,m,y=(1 - r / 255.0,1 - g / 255.0,1 - b / 255.0)
    C,M,Y,K= (c-min(c,m,y),m-min(c,m,y),y-min(c,m,y),min(c,m,y))
    return tuple(C*255,M*255,Y*255,K*255)

def cmyk2rgb (cmyk):
    C,M,Y,K= [i/255.0 for i in cmyk]
    R=C*(1-K)+K
    G=M*(1-K)+K
    B=Y*(1-K)+K
    R=(1-R)*255.0+0.5
    G=(1-G)*255.0+0.5
    B=(1-B)*255.0+0.5
    return tuple(R,G,B)

def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*255, m*255, y*255, k*255

def nonblack(inputpic):
    img = Image.open(inputpic) 
    better=Image.eval(img, lambda p: 255 * (int(p != 0))) 
    better.save('test.png')
#RGB:23,4,155
#cmyk:85,97,0,39

def test1():
    img = Image.open("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png") 
    (xdim, ydim) = img.size 
    # this assumes that no alpha-channel is set 
    black = (0, 0, 0, 0) 
    white = (255, 255, 255, 255) 
    data = img.load()
    for y in range(ydim): 
            for x in range(xdim): 
                    if data[x,y] == white: 
                            #print data[x+y*xdim]
                            data[x,y] = black
    img.save("sample-filtered.png") 

def test4():
    img = Image.open("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png") 
    (xdim, ydim) = img.size 
    # this assumes that no alpha-channel is set 
    black = (0, 0, 0, 255) 
    white = (255, 255, 255, 255) 
    data = img.load()
    for y in range(ydim): 
            for x in range(xdim): 
                    if data[x,y] == black: 
                            #print data[x+y*xdim]
                            print x,y,data[x,y]

def test2():
    img = Image.open("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png") 
    better=Image.eval(img, lambda p: 255 * (int(p != 0))) 
    better.save('test.png')
    
def test3(im1name, im2name):
    h1 = Image.open("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png").histogram()
    h2 = Image.open("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png").histogram()
    h4 = Image.open("HBR_HBR_100ng_35278_AlignmentDistribution.png").histogram()
    diff = numpy.array(h1) - numpy.array(h4)
    distance = numpy.sqrt(abs(numpy.dot(diff, diff)))
    print distance
    

def compare_images(image_file1, image_file2):
    im1 = Image.open(image_file1)
    im2 = Image.open(image_file2)
    if im1.size != im2.size:
        return 99999
    width, height = im1.size
    im_access1 = im1.load()
    im_access2 = im2.load()
    counti=0
    print counti
    for i in xrange(height):
        for j in xrange(width):
            if im_access1[i,j] != im_access2[i,j]:
                counti=counti+1
                #print counti
    print counti
    return counti/(height*width)

def getPolishedHist(imgfilename):
    img = cv2.cvtColor(cv2.imread(imgfilename),cv2.cv.CV_RGB2GRAY)
    hist_item = cv2.calcHist([img],[0],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    return hist_item

def compareh(hist1,hist2):
    distHist1 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_CORREL)
    distHist2 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_CHISQR)
    distHist3 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_INTERSECT)
    distHist4 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_BHATTACHARYYA)
    return (distHist1,distHist2,distHist3,distHist4)
    


def time1():
    h1 = Image.open("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png").histogram()
    h2 = Image.open("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png").histogram()
    diff = numpy.array(h1) - numpy.array(h2)
    distance = numpy.sqrt(abs(numpy.dot(diff, diff)))
    return distance

def time2():
    compare_images("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png", "HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    
def time3():
    hist1=getPolishedHist("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png")
    hist2=getPolishedHist("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    distHist1 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_CORREL)
    return distHist1

def time4():
    hist1=getPolishedHist("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png")
    hist2=getPolishedHist("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    distHist1 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_CHISQR)
    return distHist1

def time5():
    hist1=getPolishedHist("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png")
    hist2=getPolishedHist("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    distHist1 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_INTERSECT)
    return distHist1

def time6():
    hist1=getPolishedHist("UHR_UHR_100ng_35277_Aligned_QualityHistogram.png")
    hist2=getPolishedHist("HBR_HBR_100ng_35278_Aligned_QualityHistogram.png")
    distHist1 = cv2.compareHist(hist1,hist2,cv2.cv.CV_COMP_BHATTACHARYYA)
    return distHist1


if __name__=='__main__':
    from timeit import Timer
    t1=Timer("time1()","from __main__ import time1")
    t2=Timer("time2()","from __main__ import time2")
    t3=Timer("time3()","from __main__ import time3")
    t4=Timer("time4()","from __main__ import time4")
    t5=Timer("time5()","from __main__ import time5")
    t6=Timer("time6()","from __main__ import time6")
    print t1.timeit(10)
    print t2.timeit(10)
    print t3.timeit(10)
    print t4.timeit(10)
    print t5.timeit(10)
    print t6.timeit(10)


    