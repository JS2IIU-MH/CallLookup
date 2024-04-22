'''tkinter GUI sample
    open window with label, button and entry widgets.
'''

import datetime
import os
import shutil
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd

from adif_to_dataframe import AdifToDataFrame

NOTES_0 = 'B4.csvファイルを作成します'
NOTES_1 = 'B4callアプリは交信している相手がB4かどうかを表示するためにB4.csvファイルを使います。B4.csvファイルはWSJT-XもしくはJTDXが出力するADIFファイル(.adi)を読み込んで生成します。生成したB4.csvはB4call.exeと同じフォルダに保存します。'
NOTES_2 = '読み込ませるADIFファイルを選択してください。'
FONT_TITLE = ('Meiryo UI', '12', 'bold')
FONT_NOTE = ('Meiryo UI', '10')

MSG_WIDTH = 450

class Application(tk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.grid()

        # ファイル名
        self.adi_file = ''
        current_path, _ = os.path.split(__file__)
        self.csv_file = f'{current_path}/B4.csv'

        frame1 = tk.Frame(master)

        label1 = tk.Label(frame1, text=NOTES_0, font=FONT_TITLE)
        label1.grid()

        message1 = tk.Message(frame1, width=MSG_WIDTH, text=NOTES_1, font=FONT_NOTE)
        message1.grid()
        message2 = tk.Message(frame1, width=MSG_WIDTH, text=NOTES_2, font=FONT_NOTE)
        message2.grid(pady=10)


        frame1.grid()

        frame2 = tk.Frame(master)
        label21 = tk.Label(frame2, text='ADIF File:')
        label21.grid(row=0, column=0)

        self.label22 = tk.Label(frame2, relief=tk.SUNKEN, bg='white', width=40)
        self.label22.grid(row=0, column=1, padx=5)

        btn_file_select = tk.Button(frame2, text='...', width=4, command=self.file_select)
        btn_file_select.grid(row=0, column=2)

        frame2.grid(pady=10)

        frame3 = tk.Frame(master)
        genbtn = tk.Button(frame3, text=' B4.csvを生成する ', command=self.generate_b4csv)
        genbtn.grid(row=0, column=0, padx=20)

        extbtn = tk.Button(frame3, text=' 終了 ', command=quit)
        extbtn.grid(row=0, column=1)
        frame3.grid()
    
    def file_select(self):
        current_path, _ = os.path.split(__file__)
        filepath = filedialog.askopenfilename(
            title='Select ADIF File',
            filetypes=[('ADIF file', '.adi')],
            initialdir=current_path
        )
        self.label22['text'] = filepath
        self.adi_file = filepath

    def generate_b4csv(self):
        # ファイル存在チェック
        if os.path.isfile(self.adi_file):
            # ADIFからDataFrameに変換
            adf = AdifToDataFrame()
            all_list = adf.data_to_list(self.adi_file)
            df_adif = adf.list_to_dataframe(in_list=all_list)
            np_call = df_adif['CALL'].unique()

            # B4.csvの存在確認
            if os.path.isfile(self.csv_file):
                # 古いB4.csvが存在する場合はバックアップする
                dt_now = datetime.datetime.now()
                current_path, _ = os.path.split(__file__)
                if not os.path.isdir(f'{current_path}/backup'):
                    os.mkdir(f'{current_path}/backup')
                dst_filename = f'{current_path}/backup/{dt_now.strftime("%Y%m%d%H%M%S")}_B4.csv'
                shutil.copy(self.csv_file, dst_filename)
            
            # 新しいB4.csvを出力する
            # np.savetxt(self.csv_file, np_call, delimiter=',')
            df_call = pd.DataFrame(np_call)
            df_call.columns = ['CALL']
            df_call.to_csv(self.csv_file, index=False)

        # ボタンを非アクティブ状態にする
        


def main():
    '''example to call Application class'''

    root = tk.Tk()

    root.geometry('600x280')
    root.title('B4.csv作成ツール by JS2IIU')
    root.grid_anchor(tk.CENTER)

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()