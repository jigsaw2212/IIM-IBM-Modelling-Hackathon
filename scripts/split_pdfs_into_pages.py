import glob
import os
from multiprocessing import Pool
from pyPdf import PdfFileWriter, PdfFileReader

def f(x):
    try:
        fname = x.split('/')[-1].rstrip('.pdf')
        print '0. {}'.format(fname)
        dir = '/home/ramparkash/PAGES/' + fname
        if not os.path.exists(dir):
            os.makedirs(dir)
        x = PdfFileReader(open(x, "rb"))
        dir_len = len(os.listdir(dir))
        print '1. {}, {}, {}'.format(fname, x.numPages, dir_len)
        if x.numPages < dir_len:
            print '2. {}'.format(dir)
            for i in xrange(x.numPages):
                file = dir + '/{}_{}.pdf'.format(fname, i)
                if not os.exists.path(file):
                    y = PdfFileWriter()
                    y.addPage(x.getPage(i))
                    with open(file, "wb") as outputStream:
                        y.write(outputStream)
                    print '3. {}, {}'.format(fname, i)
    except Exception as e:
        print fname, e


if __name__ == '__main__':
    pool = Pool(5)
    files = [file for file in glob.glob('/home/ramparkash/DATA/**/*.pdf')]
    pool.map(f, files)
