
def convert_2_PNG(dataDir):
    counter = 0
    files = []
    for subdir in os.listdir(dataDir):
        for file in os.listdir(dataDir+subdir):
            if file.endswith(".tif"):
                 files.append(dataDir+subdir+'/'+file)

        if not files:
            raise Exception('No Image was found')
            
    print ('Files to process: ',len(files))
    for file in files:
        counter += 1
        subprocess.call(['gdal_translate -of PNG -b 2 -b 3 -b 4 ' + file +' '+ os.path.splitext(file)[0]+'.png'], shell=True)
        if counter % 500 == 0:
            print ('Files processed: ', counter) 
            
def split_Train_Test(dataDir):
    path = os.path.dirname(os.path.dirname(dataDir))
    shuffleFiles = "cd "+dataDir+" && for d in ./*/; do ( mkdir -p "+path+"/Test_Data/$d && cd $d && shuf -zen"+str(num)+" *.png | xargs -0 mv -t "+path+"/Test_Data/$d/ ); done"
    subprocess.call(shuffleFiles, shell=True)
