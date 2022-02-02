import math
from typing import List, Type, Optional

class Decision:#kurang . baik
    def __init__(self, decision, value):#decision= menggambar , value = anaknya menggambar
        self.decision = decision
        self.value = value

    def get_dict(self):
        return {
            'text': { 'name' : self.decision },
            'children': [self.value.get_dict()] if hasattr(self.value,'get_dict') else [{ 'text' : { 'name':self.value } }]
        }

    def get_final_values(self):#hasil akhir anak paling terakhir . aka hasil rekomendasi
        values = set()
        if hasattr(self.value,'get_final_values'):
            for val in self.value.get_final_values():
                values.add(val)
        else:
            values.add(self.value)
        return values

    def simplify(self):#hapus yang sama dari GFV
        final_val = self.get_final_values()
        if len(final_val) == 1:
            for val in final_val:
                self.value = val
        else:
            if hasattr(self.value,'simplify'):
                self.value.simplify() 
        return self

class DecisionTree:#kriteria
    def __init__(self, label, decisions, **kwargs):#label= hobi etc  , decision= menggambar etc
        self.label = label
        self.decisions = decisions
        self.kwargs = kwargs

    def get_dict(self):
        decisions = []
        for decision in self.decisions:
            decisions.append(decision.get_dict())
        ret_dict = {
            'text': { 'name': self.label },
            'children': decisions,
        }
        for key, value in self.kwargs.items():
            ret_dict[key] = value
        return ret_dict

    def get_final_values(self):
        values = set()
        for decision in self.decisions:
            if hasattr(decision.value,'get_final_values'):
                for value in decision.value.get_final_values():
                    values.add(value)
            else:
                values.add(decision.value)
        
        return values

    def simplify(self):
        for decision in self.decisions:
            decision.simplify()
        return self

class Table(): #1
    def __init__(self, datas):#, filters:dict):
        size = len(datas[0])
        self.titles = datas[0] #kolom
        datas = datas[1:]
        for data in datas:
            assert len(data) == size, 'error list size tidak sama'
        
        self.datas = datas #buang palanya
        self.target_index = len(self.titles) - 1
        self.data_set = [set() for _ in range(len(datas[0]))]
        self.data_map = [dict()  for _ in range(len(datas[0]))]
        self.inverse_data_map = [dict() for _ in range(len(datas[0]))]

        for data in datas:
            for i in range(len(data)):
                self.data_set[i].add(data[i])

        for i in range(len(datas[0])):
            index = 0
            for el in self.data_set[i]:
                self.data_map[i][el] = index
                self.inverse_data_map[i][index] = el
                index += 1

        self.total_data_target = [0 for _ in range(len(self.data_set[self.target_index]))]
        for data in datas:
            target_el_index = self.data_map[self.target_index][data[self.target_index]]
            self.total_data_target[target_el_index] += 1#total S(?)
            
    def get_decision_tree(self):
        decisions, child_tables, category = self.generate_child_tables()
        
        decision_list = []
        for i in range(len(child_tables)):#kalo mentok masuk if
            child_table = child_tables[i]
            
            _, max_gain = child_table.get_max_gain()

            if(max_gain == 0):
                max_idx = -1
                max_s = 0
                for j in range(len(child_table.total_data_target)):
                    if child_table.total_data_target[j] > max_s:
                        max_s = child_table.total_data_target[j]
                        max_idx = j

                decision_list.append(Decision(decisions[i], child_table.inverse_data_map[child_table.target_index][max_idx]))#hasil rekomen diambil dari max_idx invers
            else:
                decision_list.append(Decision(decisions[i], child_table.get_decision_tree()))  #bikin decision tree              
        
        decision_tree = DecisionTree(category, decision_list) #, datas_count=self.total_data_target, datas_s=[val for val in self.data_set[self.target_index]])

        return decision_tree

    def get_max_gain(self):
        category_list_idx = []
        for i in range(len(self.datas[0])):
            if i != self.target_index:
                category_list_idx.append(i)

        max_gain_id = -1
        max_gain = 0
        for i in category_list_idx:#CLI = id per atribut
            gain = self.gain(i)
            if gain > max_gain:
                max_gain = gain
                max_gain_id = i #REPLACE MAX GAIN
        return max_gain_id, max_gain

    def predict(self, data):
        table = self
        _, current_gain = table.get_max_gain()
        while current_gain > 0: # pengulangan buat cari tabel paling ujung
            temp_table = table.generate_child_table(data)
            if temp_table != None:
                table = temp_table
                _, current_gain = table.get_max_gain()
            else:
                break
        
        max_idx = -1
        max_s = 0
        for i in range(len(table.total_data_target)):
            if table.total_data_target[i] > max_s:
                max_s = table.total_data_target[i]
                max_idx = i
        
        return table.inverse_data_map[table.target_index][max_idx] # cari S terbanyak di tabel paling ujung

    def generate_child_table(self, data_predict):#data_predict = 1 row
        id, _ = self.get_max_gain()#id = gain tertinggi nya , ngambil atributnya
        target_id = self.target_index #
        assert id != target_id, 'target id and id cannot be the same'

        table_datas = [] #bikin tabel baru sesuai atribute max gain
        table_data_el = self.titles
        table_datas.append(table_data_el)
        for data in self.datas:
            if data[id] != data_predict[id]:#
                continue
            table_data_element = data
            table_datas.append(table_data_element)

        try:
            return Table(table_datas)
        except:
            return None

    def generate_child_tables(self):#contoh:maxgainhobi->note1.1 sampe 1.7
        id, _ = self.get_max_gain()
        target_id = self.target_index
        assert id != target_id, 'target id and id cannot be the same'

        tables = []
        tables_id = []
        for data_category in self.data_set[id]:
            tables_id.append(data_category)
            table_datas = []
            table_data_el = self.titles
            table_datas.append(table_data_el)
            for data in self.datas:
                if data[id] != data_category:
                    continue
                table_data_element = data
                table_datas.append(table_data_element)

            tables.append(Table(table_datas))
            del table_datas
            del table_data_el
        return tables_id, tables, self.titles[id]

    def entrophy_total(self):#bpkny entropy
        total = sum(self.total_data_target)#100
        entropy = 0
        for count in self.total_data_target:#8 / sesuai total fakultas
            entropy += math.log2(float(count)/total) * -(float(count)/total)
        return entropy

    def s_i(self, category_idx, target_el):#category_idx=butawarna.etc , target_el=fakultas
        ret_dict = dict()
        for data_el in self.data_set[category_idx]:
            ret_dict[data_el] = 0
            for data in self.datas:
                if data[self.target_index] == target_el and data[category_idx] == data_el:
                    ret_dict[data_el] += 1
        return ret_dict#ret_dict=(ya:x , tidak:x)

    def s(self, category_idx):#category_id = atribut , 
        dict_list = [dict() for _ in range(len(self.data_set[self.target_index]))]
        idx = 0
        for data in self.data_set[self.target_index]:
            dict_list[idx] = self.s_i(category_idx, data)
            idx += 1 #dict_list,(fakultas:butawarna:ya:totalya.totaltidak) + semua fakultas

        final_dict = dict()
        for k, _ in dict_list[0].items():
            final_dict[k] = 0

        for dict_el in dict_list:
            for k, v in dict_el.items():
                final_dict[k] += v #total butawarna per fakultas

        return final_dict #atribut(cabang atribut,totalnya)

    def entropy_category(self, category_idx):
        total = self.s(category_idx)
        target_dict = [dict() for _ in range(len(self.data_set[self.target_index]))]
        idx = 0
        for target in self.data_set[self.target_index]:
            target_dict[idx] = self.s_i(category_idx, target)#self.s_i(butawrnaetc,ekonomi)
            idx += 1 #target_dict[idx]=[tidak/ya:totalpercategorycabang]

        entropy = dict()
        for key in self.data_set[category_idx]:#(8)
            entropy[key] = 0

        for t_d in target_dict:
            for k, v in t_d.items():#k=ya/tdk , v=total ya/tdk
                if v == 0: continue
                entropy[k] += math.log2(v/total[k]) * -(v/total[k]) #entropy per atribut cabangnya(ya/tdk)

        return entropy

    def gain(self, category_idx):
        entropy_total = self.entrophy_total()#bapaknya entropy
        total = sum(self.total_data_target)
        gain = 0

        s = self.s(category_idx) #s=total per atribut , s_i= total per fakultas
        entropy = self.entropy_category(category_idx)#entropy per kategory pet cabang

        for k, _ in s.items():#s , ya/tidak
            gain += (float(s[k])/total) * entropy[k]#rumus gain per atribut

        gain = entropy_total - gain
        return gain


    def __str__(self):
        ret = ''
        for data in self.datas:
            ret += str(data) + '\n'
        return ret

from data import data, get_data, get_data_filtered #ambil data
# table = Table(data) # index terakhir
# biologi = 0
# for i in table.datas:
#     if i[6] == 'Kurang':
#         biologi += 1
# print(biologi)
# print(table.data_set[table.target_index])
#table_anak = table.generate_child_table(('Tidak', 'Menggambar'))
#for i in range(len(table.data_set)):
#    print(table_anak.gain(i))
#    print(table_anak.titles[i])
#kimia = [0 for _ in range(8)]
#print(table_anak.data_set[8])
#for i in table_anak.datas:
#    if i[7] == 'Kurang':
#        kimia[table_anak.data_map[8][i[8]]] += 1
#print(table_anak.entropy_category(7))
#print(kimia)
#print(len(table_anak.datas))

# #            Buta warna	    Hobi        Mat	        Pkn	    Tik	    Fisika	Biologi	  Kimia
# predict_wil = ('Ya', 'Bersosialisasi', 'Baik', 'Kurang', 'Kurang', 'Kurang', 'Baik', 'Kurang')

# print(table.predict(predict_wil))

#import json
# json_data = json.dump(table.get_decision_tree().get_dict(), open('decision_table.json', 'w'))
# json_data = json.dump(table.get_decision_tree().simplify().get_dict(), open('decision_table_simple.json', 'w'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware( 
    CORSMiddleware,
    allow_origins=['*'], #request dari website tertentu
    allow_credentials=True, 
    allow_methods=["*"],#post get
    allow_headers=["*"],
)

table = None
last_count = -1

@app.get("/predict")
def predict(buta_warna: str, hobi: str, mat: str, pkn: str, tik: str, fisika: str, biologi: str, kimia: str, count: Optional[int]=0):
    global last_count
    global table
    if count != last_count:
        if count == 0:
            table = Table(get_data())
        else:
            table = Table(get_data_filtered(count))
    last_count = count
    prediction = (buta_warna, hobi, mat, pkn, tik, fisika, biologi, kimia)

    return table.predict(prediction) #return hasil rekomendasi

@app.get("/decisiontree")
def decisiontree(count: Optional[int]=0):
    global last_count
    global table
    if count != last_count:
        if count == 0:
            table = Table(get_data())
        else:
            table = Table(get_data_filtered(count))

    last_count = count
    return table.get_decision_tree().simplify().get_dict()
 
