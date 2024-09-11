import json, random
import os
import numpy as np
import pdb


def read_data(instrument, foils_path, images_path, data_root):
    if instrument == "vqa":
        foils_data = read_vqa(foils_path, data_root)
    elif instrument in ["gqa", "gqa_balanced"]:
        foils_data = read_gqa(foils_path)
    elif instrument == "nlvr2":
        foils_data = read_nlvr2(foils_path, images_path)
    elif instrument == "clevr":
        foils_data = read_clevr(foils_path, images_path)
    elif "original-foil-dataset" in foils_path:
        foils_data = read_foil_dataset(foils_path)
    else:
        with open(foils_path) as json_file:
            foils_data = json.load(json_file)
    return foils_data


def read_foil_dataset(foils_path):
    """
    Read in the data of the original foil dataset and convert it on the fly to our format (dict/json).
    """
    with open(foils_path) as json_file:
        foil_dataset = json.load(json_file)

    foils_data = {}  # our format

    for foil in foil_dataset['annotations']:
        # For unimodal models, we always need foil, non-foil pairs to compare perplexity.
        if foil['foil'] == True:  # we have a foil not foil pair
            # recover the original sentence
            orig_sentence = foil['caption'].replace(
                foil['foil_word'], foil['target_word'])
            image_id = foil['image_id']
            foils_data[foil["foil_id"]] = {'dataset': 'FOIL dataset',
                                           'dataset_idx': foil["foil_id"],
                                           'original_split': 'test',
                                           'linguistic_phenomena': 'noun phrases',
                                           # COCO_val2014_000000522703.jpg all are "val"
                                           'image_file': f'COCO_val2014_{str(image_id).zfill(12)}.jpg',
                                           'caption': orig_sentence,
                                           'foils': [foil['caption']],
                                           'classes': foil['target_word'],
                                           'classes_foil': foil['foil_word'],
                                           }
        if len(foils_data) > 1500:
            break
    return foils_data


def read_vqa(vqa_path, data_root):
    """
    Read in the VQA 2.0 data and transform it into our foiling format.
    Input json looks like:
    {'image_id': 535754, 'question': 'Does the statue have glasses on?', 'question_id': 535754002},
    """
    foils_data = {}
    split = 'val'
    annotations_path = f'{data_root}VQA2.0/v2_mscoco_val2014_annotations.json'

    with open(annotations_path) as json_file:
        vqa_anno = json.load(json_file)
        # print(vqa_anno.keys())
        # print(vqa_anno['annotations'])
        imgToQA = {ann['image_id']: [] for ann in vqa_anno['annotations']}
        qa =  {ann['question_id']:       [] for ann in vqa_anno['annotations']}
        for ann in vqa_anno['annotations']:
            imgToQA[ann['image_id']] += [ann]
            qa[ann['question_id']] = ann

    with open(vqa_path) as json_file:
        vqa_data = json.load(json_file)
        # there are 81,434 images. Subsample 1k of them
        np.random.seed(0)
        subsample = np.random.choice(
            len(vqa_data['questions']), 300, replace=False)
        # print(foils_data.keys())
        for i in subsample:
            sample = vqa_data['questions'][i]
            image_id = sample['image_id']
            question = sample['question']
            question_id = sample['question_id']
            answer = qa[question_id]['multiple_choice_answer']
            # print(image_id, question, question_id)
            foils_data[image_id] = {'dataset': 'vqa',
                                    # 'dataset_idx': foil["foil_id"],
                                    # 'original_split': split,
                                    # 'linguistic_phenomena': 'noun phrases',
                                    # COCO_val2014_000000522703.jpg all are "val"
                                    'image_file': f'COCO_{split}2014_{str(image_id).zfill(12)}.jpg',
                                    'caption': question,
                                    'answer': answer,
                                    'answers': [x['answer'] for x in qa[question_id]['answers']]
                                    # 'foils': [foil['caption']],
                                    # 'classes': foil['target_word'],
                                    # 'classes_foil': foil['foil_word'],
                                    }

    return foils_data


def read_gqa(gqa_path):
    """
    Read in the GQA data and transform it into our foiling format.
    Input json looks like:
    """
    foils_data = {}
    split = 'val'
    np.random.seed(0)
    
    """
    (Pdb) gqa_data['12344808']
    {'semantic': [{'operation': 'select', 'dependencies': [], 'argument': 'boy (-)'},
    {'operation': 'exist', 'dependencies': [0], 'argument': '?'},
    {'operation': 'select', 'dependencies': [], 'argument': 'farmers (-) '},
    {'operation': 'exist', 'dependencies': [2], 'argument': '?'},
    {'operation': 'or', 'dependencies': [1, 3], 'argument': ''}],
    'entailed': ['12344827', '12344556', '12344807', '12344828', '12344593', '12344679'],
    'equivalent': ['12344808'],
    'question': 'Are there either any farmers or boys in the picture?',
    'imageId': '2399672',
    'isBalanced': False,
    'groups': {'global': None, 'local': '09existOr-boy_farmers'},
    'answer': 'no',
    'semanticStr': 'select: boy (-)->exist: ? [0]->select: farmers (-) ->exist: ? [2]->or:  [1, 3]',
    'annotations': {'answer': {}, 'question': {}, 'fullAnswer': {}},
    'types': {'detailed': 'existOrC', 'semantic': 'obj', 'structural': 'logical'},
    'fullAnswer': 'No, there are no farmers or boys.'}
    """

    with open(gqa_path) as json_file:
        gqa_data = json.load(json_file)
        # print(f'There are {len(gqa_data)} to choose from.')
        # there are 81,434 images. Subsample 300 of them
        gqa_data = dict(random.sample(sorted(gqa_data.items()), 300))  # 100
        
        for idx, sample in gqa_data.items():
            # sample = gqa_data['questions'][i]
            # image_id = sample['image_id']
            question = sample['question']
            answer = sample['answer']
            # print(image_id, question, question_id)
            foils_data[idx] = {'dataset': 'gqa',
                               'dataset_idx': idx,
                               # 'original_split': split,
                               # 'linguistic_phenomena': 'noun phrases',
                               # COCO_val2014_000000522703.jpg all are "val"
                               'image_file': f'{sample["imageId"]}.jpg',
                               'caption': question,
                               'answer': answer,
                               # 'foils': [foil['caption']],
                               # 'classes': foil['target_word'],
                               # 'classes_foil': foil['foil_word'],
                               }
    return foils_data


def read_nlvr2(nlvr_path, images_root):
    """
    Read in the NLVR2 data and transform it into our foiling format.
    Input json looks like:

    """
    foils_data = {}
    split = 'test'

    with open(nlvr_path) as json_file:
        nlvr_data = [json.loads(line) for line in json_file.readlines()]
        # there are 81,434 images. Subsample 1k of them
        np.random.seed(0)
        # TODO increase this number!
        subsample = np.random.choice(len(nlvr_data), 1500, replace=False)
        # print(foils_data.keys())
        for i in subsample:
            sample = nlvr_data[i]
            for k in [0, 1]:  # 0 is left image, 1 is right
                image_id = sample['identifier']
                sentence = sample['sentence']
                # print(image_id, question, question_id)
                image_path = f'{sample["identifier"][:-2]}-img{k}.png'
                # many images can not be downloaded anymore for NLVR2
                if os.path.isfile(os.path.join(images_root, image_path)):
                    foils_data[image_id] = {'dataset': 'nlvr2',
                                            # 'dataset_idx': foil["foil_id"],
                                            # 'original_split': split,
                                            # 'linguistic_phenomena': 'noun phrases',
                                            # COCO_val2014_000000522703.jpg all are "val"
                                            'image_file': image_path,
                                            'caption': sentence,
                                            'label': sample['label']
                                            # 'foils': [foil['caption']],
                                            # 'classes': foil['target_word'],
                                            # 'classes_foil': foil['foil_word'],
                                            }
    return foils_data

def read_clevr(clevr_path, images_root):
    """
    Read in the CLEVR data and transform it into our foiling format.

    """
    foils_data = {}
    # pdb.set_trace()

    with open(clevr_path) as json_file:
        clevr_data = json.load(json_file)
        # there are 70,000 images. Subsample 300 of them
        np.random.seed(0)
        subsample = np.random.choice(
            len(clevr_data['questions']), 300, replace=False)
        # print(foils_data.keys())
        for i in subsample:
            sample = clevr_data['questions'][i]
            image_id = sample['image_index']
            question = sample['question']
            # print(image_id, question, question_id)
            image_path = f'{sample["image_filename"]}'

            if os.path.isfile(os.path.join(images_root, image_path)):
                foils_data[image_id] = {'dataset': 'clevr',
                                        'image_file': image_path,
                                        'caption': question,
                                        'answer': sample['answer']
                                        }
    return foils_data

if __name__ == "__main__":
    # gqa = ["./dataset/GQA/images/", "./dataset/GQA/val_all_questions.json"]
    # read_data('gqa', gqa[1], gqa[0], "./dataset/")
    clevr = ["./dataset/clevr/CLEVR_v1.0/images/train/",
             "./dataset/clevr/CLEVR_v1.0/questions/CLEVR_train_questions.json"]
    read_data('clevr', clevr[1], clevr[0], "./dataset/")