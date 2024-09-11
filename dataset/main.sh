# wget https://downloads.cs.stanford.edu/nlp/data/gqa/images.zip
# wget https://downloads.cs.stanford.edu/nlp/data/gqa/questions1.2.zip

# mkdir GQA
# mv images.zip GQA/images.zip
# mv questions1.2.zip GQA/questions1.2.zip
# unzip GQA/images.zip
# unzip GQA/questions1.2.zip

# rm -rf GQA/images.zip GQA/questions1.2.zip

# wget http://images.cocodataset.org/zips/val2014.zip

# mkdir COCO
# unzip val2014.zip
# rm -rf val2014.zip
# mv val2014 COCO/val2014

# wget https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Val_mscoco.zip
# wget https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Val_mscoco.zip
# mkdir VQA2.0
# unzip v2_Questions_Val_mscoco.zip
# unzip v2_Annotations_Val_mscoco.zip
# rm -rf v2_Questions_Val_mscoco.zip v2_Annotations_Val_mscoco.zip
# mv v2_mscoco_val2014_annotations.json VQA2.0/v2_mscoco_val2014_annotations.json
# mv v2_OpenEnded_mscoco_val2014_questions.json VQA2.0/v2_OpenEnded_mscoco_val2014_questions.json

# wget https://www.dropbox.com/s/bsmowpgz43pwkyd/foilv1.0_train_2017.json
# wget https://www.dropbox.com/s/u4ntgo73szg6yai/foilv1.0_test_2017.json

# wget http://vision.stanford.edu/yukezhu/visual7w_images.zip
# mkdir visual7w
# unzip visual7w_images.zip -d visual7w
# rm -rf visual7w_images.zip

# wget https://ai.stanford.edu/~yukez/papers/resources/dataset_v7w_telling.zip
# wget https://ai.stanford.edu/~yukez/papers/resources/dataset_v7w_pointing.zip
# unzip dataset_v7w_telling.zip -d visual7w
# unzip dataset_v7w_pointing.zip -d visual7w
# rm -rf dataset_v7w_telling.zip dataset_v7w_pointing.zip

wget https://dl.fbaipublicfiles.com/clevr/CLEVR_v1.0.zip
unzip CLEVR_v1.0.zip -d clevr
rm -rf CLEVR_v1.0.zip