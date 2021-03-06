# author：chenhanping
# date 2018/12/3 上午10:44
# copyright ustc sse
import json
import os
from keras.preprocessing.text import *
from keras.preprocessing import sequence
import numpy as np


def load_data(config_file_path="../config/path_config.json", load_val=False, get_token=False, one_hot=True):
    """
    加载数据
    :param get_token:
    :param load_val:
    :param config_file_path:
    :return:
    """
    tokenizer = Tokenizer(num_words=20)
    with open(config_file_path, 'r') as f:
        paths = json.load(f)
    label_path = paths['label_path']
    protein_seq_path = paths['protein_seq_path']
    x, y, max_len = read_data(protein_seq_path, label_path)
    texts = list()
    for s in x:
        text = ""
        for c in s:
            text += c + " "
        texts.append(text)
    tokenizer.fit_on_texts(texts)
    print(tokenizer.word_counts)
    print(tokenizer.word_index)
    x_seq = tokenizer.texts_to_sequences(texts)
    x_seq = sequence.pad_sequences(x_seq, maxlen=max_len, padding='post')
    y = sequence.pad_sequences(y, maxlen=max_len, padding='post')
    if one_hot:
        y = np.expand_dims(y, axis=2)
    print(np.shape(x_seq), np.shape(y))
    if load_val:
        val_label_path = paths['dset72_label_path']
        val_seq_path = paths['dset72_protein_seq_path']
        val_x, val_y, _ = read_data(val_seq_path, val_label_path)
        val_texts = list()
        for s in val_x:
            text = ""
            for c in s:
                text += c + " "
            val_texts.append(text)
        val_x_seq = tokenizer.texts_to_sequences(val_texts)
        val_x_seq = sequence.pad_sequences(val_x_seq, maxlen=max_len,padding='post')
        val_y = sequence.pad_sequences(val_y, maxlen=max_len,padding='post')
        if one_hot:
            val_y = np.expand_dims(val_y, axis=2)
        print(np.shape(val_x_seq), np.shape(val_y))
        if get_token:
            return x_seq, y, val_x_seq, val_y, tokenizer
        return x_seq, y, val_x_seq, val_y
    if get_token:
        return x_seq, y, tokenizer
    return x_seq, y


def read_data(seq_path, label_path):
    max_len = 0
    protein_file_list = os.listdir(seq_path)
    x = []
    y = []
    for file in protein_file_list:
        file_path = os.path.join(seq_path, file)
        filename, _ = os.path.splitext(file)
        f = open(file_path, 'r')
        seq = f.readline()
        if len(seq) > 300:
            continue
        label_file_path = os.path.join(label_path, filename+".txt")
        f = open(label_file_path, 'r')
        label = [int(x) for x in f.readline()]

        if len(seq) > max_len:
            max_len = len(seq)
        x.append(seq)
        y.append(label)
    return x, y, max_len


def create_label(config_file_path="../config/path_config.json"):
    with open(config_file_path, 'r') as f:
        paths = json.load(f)
    data_directory = paths['data_directory']
    label_path = os.path.join(data_directory, "label")
    protein_seq_path = os.path.join(data_directory, "protein_seq")
    index_dict_path = os.path.join(data_directory, "index_dict")
    if not os.path.exists(label_path):
        os.makedirs(label_path)
    site_set_path = os.path.join(data_directory, "site_set")
    protein_file_list = os.listdir(protein_seq_path)

    for file in protein_file_list:
        label = ""
        filename, _ = os.path.splitext(file)
        index_dict_file = os.path.join(index_dict_path, filename+".json")
        site_set_file = os.path.join(site_set_path, filename + ".txt")
        print(filename)
        with open(site_set_file, 'r') as f:
            line = f.readline()
            if len(line) > 0:
                site_arr = [int(x) for x in line.split(',')]
            else:
                site_arr = []
        site_set = set(site_arr)
        with open(index_dict_file, 'r') as f:
            index_dict = json.load(f)
        for res_id, _ in index_dict.items():
            if int(res_id) in site_set:
                label += '1'
            else:
                label += '0'
        label_file_path = os.path.join(label_path, filename+".txt")
        print(filename, label, len(label))
        # 保存
        f = open(label_file_path, 'w')
        f.write(label)


def filter_protein_seq(config_file_path="../config/path_config.json"):
    with open(config_file_path, 'r') as f:
        paths = json.load(f)
    data_directory = paths['data_directory']
    seq_path = os.path.join(data_directory, "protein_seq")
    site_path = paths['site_path']
    val_seq_path = paths['val_protein_seq_path']
    seq_file_list = os.listdir(seq_path)
    count = 0
    for file in seq_file_list:
        # if not os.path.exists(os.path.join(site_path, file)):
        #     print(os.path.join(seq_path, file))
        #     os.remove(os.path.join(seq_path, file))
        #     count += 1
        if os.path.exists(os.path.join(val_seq_path, file)):
            count += 1
            print(os.path.join(val_seq_path, file))
            os.remove(os.path.join(seq_path, file))
    print(count)




if __name__ == '__main__':
    create_label()
    # filter_protein_seq()