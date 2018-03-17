# This software is released under the MIT License, see LICENSE.txt.

import numpy as np
import os
import hashlib

class Bloomfilter:
    def __init__(self, number, size):
        # number : いくつkey以外のフェイクをハッシュ関数に通すか、これが増えるとより匿名性が増し計算量や通過する量が増える
        # size : フィルタのサイズをどうするか、大きいと匿名性が増し計算量や通過する量が増える
        self.number = number
        self.size = size
    
    # キーからフィルタを作成する関数
    def create_filter(self, key):
        self.filter = np.zeros(size)
        # 適当にランダムなフェイクを作成する
        random = [os.urandom(1) for _ in range(self.number)]
        random.append(key)
        for rand_key in random:
            # md5を利用し、フィルタを埋めていく
            key_num = int(hashlib.md5(rand_key).hexdigest(),16)
            # 一つのキーにつき３つフィルタを埋める
            for _ in range(3):
                match_num, key_num = key_num % size, key_num // size
                # 対応する部分のみ1以上にしていきたい
                self.filter[match_num] += 1
        return self.filter
    
    # フィルタから当てはまるか確かめる関数
    def check_filter(self, check_list):
        # ここに当てはまる単語を入れていく
        option_list = []
        # 確かめたいキーに対してもフィルタを作成したときと同じ処理を行う
        for check_key in check_list:
            key_num = int(hashlib.md5(check_key).hexdigest(),16)
            check_indexs = []
            for _ in range(3):
                match_num, key_num = key_num % size, key_num // size
                check_indexs.append(match_num)
            # もし全てのインデックスにおいてfilterの値が1以上であればフィルターを追加
            # option_listに追加していく
            if all(self.filter[check_index] for check_index in check_indexs):
                option_list.append(check_key)
        return option_list

number = 10
size = 100
key = "http://kawai_bitcoin"
bloomfilter = Bloomfilter(number, size)

fil = bloomfilter.create_filter(key.encode())
print(fil)

# 確認用は適当に30個にしてみた
check_list = [os.urandom(1) for _ in range(30)]
check_list.append(key.encode())
option = bloomfilter.check_filter(check_list)
print(option)