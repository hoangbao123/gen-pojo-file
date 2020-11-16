from class_data import ClassData
import json 

def gen_var_name(original_name):
    values = original_name.split("_")
    if len(values) == 1:
        return original_name
    else:
        class_name = values[0]
        for i in range(1, len(values)):
            class_name += values[i].capitalize()
        return class_name

def gen_class_name(original_name):
    values = original_name.split("_")
    class_name = ""
    for i in range(0, len(values)):
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
            

def gen_pojo_from_object(source_object, class_name):
    if isinstance(source_object, dict):
        new_class = ClassData(class_name)
        current_attr = []
        inner_class_dict = {}
        for k, v in source_object.items():
            if isinstance(v, int):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), 'int', True, True, True))
            elif isinstance(v, float):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), 'double', True, True, True))
            elif isinstance(v, str):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), 'String', True, True, True))
            elif isinstance(v, bool):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), 'Boolean', True, True, True))
            elif isinstance(v, list):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), f'List<{gen_class_name(k)}>', True, True, True))
                inner_class = gen_pojo_from_object(v[0], gen_class_name(k))
                inner_class_dict[f'List<{gen_class_name(k)}>'] = inner_class
            elif isinstance(v, dict):
                current_attr.append(gen_attr_dict(k, gen_var_name(k), gen_class_name(k), True, True, True))
                inner_class = gen_pojo_from_object(v, gen_class_name(k))
                inner_class_dict[gen_class_name(k)] = inner_class
        new_class.class_attributes = current_attr
        new_class.inner_class = inner_class_dict
        return new_class


def gen_pojo_from_json(source_file, class_name="random"):
    f = open(source_file)
    data = json.load(f)
    need_class = gen_pojo_from_object(data, class_name)
    need_class.gen_class_file('java')
    

def gen_pojo_from_list(li):
    pass 


def gen_pojo_from_dict(li):
    pass


if __name__ == "__main__":
#    gen_pojo("/home/hoangbao/workspace/utils/raw_data/v1.txt")
    gen_pojo_from_json("raw_data/data.json")