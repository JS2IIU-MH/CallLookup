''' adif_to_dataframe.py '''

import re
import pandas as pd


class AdifToDataFrame():
    '''generate DataFrame from adif file '''
    def __init__(self) -> None:
        # set default
        self.column_list = [
            'CALL', 'MODE', 'BAND', 'FREQ', 'GRIDSQUARE', 'QSO_DATE', 'TIME_ON',
            'QSO_DATE_OFF', 'TIME_OFF',
            'RST_RCVD', 'RST_SENT', 'STATION_CALLSIGN', 'MY_GRIDSQUARE',
            'COMMENT', 'SUBMODE', 'EQSL_QSL_SENT']
        self.set_default_columns = set(self.column_list)

    @classmethod
    def data_to_list(cls, filepath):
        ''' class method: adif.adi file to string list '''
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                out_list = f.readlines()
        except FileNotFoundError:
            print('file not found.')
            return -1

        return out_list

    def list_to_dataframe(self, in_list):
        ''' adif file lines (in_list) convert to pd.DataFrame '''

        # output dataframe
        out_df = pd.DataFrame()
        row_count = 0

        # matching patterns
        p_end_of_record = re.compile(r'<EOR>')
        p_adif_tag = re.compile(r'<(\w+):([0-9]+)>')

        # デフォルトのcolumnsリスト以外のタグがあった場合にはそれを追加するための処置
        # generate DataFrame columns
        set_index = {'CALL', 'EQSL_QSL_SENT'}
        for line_record in in_list:
            if re.findall(p_end_of_record, string=line_record):
                res = re.findall(pattern=p_adif_tag, string=line_record)
                for _ in range(len(res)):
                    set_index.add(res.pop()[0].upper())

        # setの差集合
        set_def = set_index - self.set_default_columns

        self.column_list = self.column_list + list(set_def)
        # self.column_list.sort()
        print(self.column_list)

        for s in in_list:
            if p_end_of_record.search(s.upper()) is not None:
                tmp_df = pd.DataFrame(columns=self.column_list)
                tmp_iter = p_adif_tag.finditer(s)
                # tmp_iterはマッチしたすべての部分を含むイテレータ
                # イテレータオブジェクト.span()で文字列位置のタプル
                # イテレータオブジェクト.stringで元の文字列全体
                for tmp in tmp_iter:
                    tmp_df.at[str(row_count), tmp.group(1).upper()]\
                        = tmp.string[tmp.span()[1]:tmp.span()[1]+int(tmp.group(2))]
                row_count += 1

                tmp_df = tmp_df.fillna('N/A')

                # print(tmp_dict)
                # print(tmp_df)
                out_df = pd.concat([out_df, tmp_df])

        return out_df


def main():
    ''' main func for test purpose '''
    sample_file = 'sample_adif.adi'
    # sample_file = '2023-10-16_213417_wsjtx_log.adi'
    # output_csv_file = 'adif_data.csv'

    adif2df = AdifToDataFrame()

    all_list = adif2df.data_to_list(sample_file)

    df_adif = adif2df.list_to_dataframe(in_list=all_list)

    print(df_adif)

    # df_adif.to_csv(output_csv_file)


if __name__ == '__main__':
    main()
