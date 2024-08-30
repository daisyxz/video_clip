class ExcelDataMat:
    filed_idx_map = dict()
    data_mat = list()


    def setFiledIdxMap(self, filed_idx_map):
        self.filed_idx_map = filed_idx_map

    def setDataMat(self, data_mat):
        self.data_mat = data_mat

    def __init__(self, filed_idx_map,data_mat):
        self.filed_idx_map = filed_idx_map
        # 如传入data_mat为二维将numpy数组转成二维list，便于后续使用
        self.data_mat = data_mat
        self.data_mat = list()
        for line in data_mat:
            new_line = list()
            for e in line:
                new_line.append(e)
            self.data_mat.append(new_line)



    def submatByFileds(self, fileds):
        write_data_mat = list()
        for i in range(len(self.data_mat)):
            line = list()
            for f in fileds:
                line.append(self.data_mat[i][self.filed_idx_map[f]])
            write_data_mat.append(line)
        return write_data_mat

    def changeColumnName(self, src_name, dst_name):
        feed_batck_idx = self.filed_idx_map[src_name]
        del self.filed_idx_map[src_name]
        self.filed_idx_map[dst_name] = feed_batck_idx
        return feed_batck_idx

    # 20230915
    def getColumnNames(self):
        id_to_field = {self.filed_idx_map[f]:f for f in self.filed_idx_map.keys()}
        return [id_to_field[i] for i in range(len(id_to_field))]


    # remove repeat column
    def removeRepeatColumn(self, key_column, type, p1):
        key_idx = self.filed_idx_map[key_column]
        line_cnt = dict()
        for line in self.data_mat:
            key = line[key_idx]
            if key in line_cnt.keys():
                line_cnt[key] +=1
            else:
                line_cnt[key] = 1
        # for k in line_cnt.keys():
        #     if line_cnt[k] > 1:
        #         print('kkk=' + k)
        new_data_mat = [l for l in self.data_mat if line_cnt[l[key_idx]]==1]
        repeat_data = [l for l in self.data_mat if line_cnt[l[key_idx]]>1]
        after_repeat_remove_data = list()
        if type == "rand":
            key_set = set()
            for line in repeat_data:
                if line[key_idx] not in key_set:
                    after_repeat_remove_data.append(line)
                    key_set.add(line[key_idx])
        elif type == "max":
            max_value_dict = dict()
            for line in repeat_data:
                key = line[key_idx]
                if key not in max_value_dict.keys():
                    max_value_dict[key] = line
                else:
                    idx = self.filed_idx_map[p1]
                    value = line[idx]
                    value_in_dict = max_value_dict[key][idx]
                    if value > value_in_dict:
                        max_value_dict[key] = line
            after_repeat_remove_data = [max_value_dict[k] for k in max_value_dict.keys()]
        else:
            print('[ERROR] invalid type for remove repeat column')
            return
        print("new_data_mat shape:" + str(len(new_data_mat)))
        print("after shape:" + str(len(after_repeat_remove_data)))
        self.data_mat = new_data_mat + after_repeat_remove_data
        return




