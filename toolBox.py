import codecs
import os
import re
import csv
import chardet
import emoji
import pandas as pd
import neologdn
import spacy


def find_encoding(file):
    r_file = open(file, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc


def read_to_df(file, encode, header=None):
    with codecs.open(file, "r", encode, "ignore") as f:
        df = pd.read_table(f, delimiter="\t", header=header)
    return df


def read_to_list(file, encode):
    with open(file, 'r', encoding=encode) as f:
        reader = csv.reader(f)
        word_list = list(reader)
        return word_list


def filtered_df(df):
    temp_df = df[~df["送信者ID[msg.userId]"].str.contains("dummy-", na=False)]
    new_df = temp_df[~temp_df["送信者ID[msg.userId]"].str.startswith("u", na=False)]
    return new_df


def pre_process(text_list):
    result = []
    for text in text_list:
        if not isinstance(text, str):
            text = str(text)
        # normalized_text = neologdn.normalize(text)
        text_no_url = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text)
        text_no_emoji = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text_no_url])
        text_no_n = text_no_emoji.replace("\n", "")
        # tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', text_no_emoji)
        # text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
        result.append(text_no_n)
    return result


def add_stop_words(customize_stop_words, nlp):
    for w in customize_stop_words:
        nlp.vocab[w[0]].is_stop = True


def write_to_csv(df, output_filename):
    labels = ["Name","Location","Address","Phone","Email","RoomId","MsgId","Msg"]
    df = df.reindex(labels, axis=1)
    df.to_csv(output_filename, sep="\t", index=False)
    print("Successfully wrote df to csv file")


def write_to_xlsx(df, output_filename):
    labels = ["Name","Location","Address","Phone","Email","RoomId","MsgId","Msg"]
    df = df.reindex(labels, axis=1)
    with pd.ExcelWriter(output_filename) as writer:
        df.to_excel(writer, sheet_name=output_filename, index=False)
    print("Successfully wrote df to excel file")


if __name__=="__main__":
    stop_keys = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\StopKey_v01.csv"
    # file_path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    file_path = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809).csv"
    df = read_to_df(file_path, find_encoding(file_path))
    df = filtered_df(df)

    # text = "お友達の紹介で、女子２人で三時のティータイムに利用しました。2人用のソファに並んでいただきま〜す v(^^)v なかよし（笑" \
    #        "最後に出された,モンブランのｹｰｷ。" \
    #        "やばっっっ！！これはうまーーーい!!" \
    #        "とってもＤｅｌｉｃｉｏｕｓで、サービスもGoodでした😀" \
    #        "これで2,500円はとってもお得です☆" \
    #        "http://hogehoge.nantoka.blog/example/link.html"


