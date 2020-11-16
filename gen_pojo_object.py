from class_data import ClassData


def gen_var_name(original_name):
    values = original_name.split("_")
    if len(values) == 1:
        return original_name
    else:
        class_name = values[0]
        for i in range(1, len(values)):
            class_name += values[i].capitalize()
        return class_name


def gen_attr_dict(original_name, generated_name, data_type, column=True, gson=True, jackson=True):
    if original_name == generated_name:
        return {
            "name": original_name,
            "data_type": data_type,
            "column": None,
            "gson": None,
            "jackson": None
        }
    else:
        return {
            "name": generated_name,
            "data_type": data_type,
            "column": original_name  if column else None,
            "gson": original_name if gson else None,
            "jackson": original_name if jackson  else None
        }


def gen_pojo(source_file, source_type='db-diagram'):
    with open(source_file) as f:
        current_class = None
        current_class_attr = []
        for line in f:    
            if line.strip == "":
                continue
            elif line.startswith("Table"):
                line = line.replace("Table", "").replace("\n", "").replace("{", "").strip(" ")
                class_name = gen_var_name(line)
                new_class = ClassData(class_name)
                current_class = new_class
            elif line.replace("\n", "").strip(" ") == "}":
                if current_class is None:
                    continue
                else:
                    current_class.class_attributes = current_class_attr
                    current_class.gen_class_file()
                    current_class = None
                    current_class_attr = []     
            else:
                if current_class is None:
                    continue
                else:
                    values = line.replace("\n", "").strip(" ").split(" ")
                    if values[0] == '':
                        continue
                    if len(values) < 2:
                        raise ValueError(f"Can not parse var name and var type from this {line}")
                    attr_name = gen_var_name(values[0])
                    attr_data = values[1]
                    attr_dict = gen_attr_dict(values[0], attr_name, attr_data, True, True, True)
                    current_class_attr.append(attr_dict)
            
            
                       
if __name__ == "__main__":
   gen_pojo("/home/hoangbao/workspace/utils/raw_data/v1.txt")