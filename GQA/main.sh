# http://mscoco.org/dataset/#download
# https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Train_mscoco.zip
# https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Val_mscoco.zip

# https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Train_mscoco.zip
# https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Val_mscoco.zip

# https://cs.stanford.edu/people/dorarad/gqa/download.html

wget https://downloads.cs.stanford.edu/nlp/data/gqa/images.zip
wget https://downloads.cs.stanford.edu/nlp/data/gqa/questions1.2.zip

unzip images.zip
unzip questions1.2.zip

rm -rf images.zip questions1.2.zip