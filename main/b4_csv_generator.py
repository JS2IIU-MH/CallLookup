'''tkinter GUI sample
    open window with label, button and entry widgets.
'''

import tkinter as tk

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
        self.csv_file = ''

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

        label22 = tk.Label(frame2, relief=tk.SUNKEN, bg='white', width=40)
        label22.grid(row=0, column=1, padx=5)

        btn_file_select = tk.Button(frame2, text='...', width=4, command=self.file_select)
        btn_file_select.grid(row=0, column=2)

        frame2.grid(pady=10)

        frame3 = tk.Frame(master)
        genbtn = tk.Button(frame3, text='B4.csvを生成する', command=self.generate_b4csv)
        genbtn.grid(row=0, column=0, padx=20)

        extbtn = tk.Button(frame3, text='キャンセル', command=quit)
        extbtn.grid(row=0, column=1)
        frame3.grid()
    
    def file_select(self):
        pass

    def generate_b4csv(self):
        pass


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