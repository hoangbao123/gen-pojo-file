from typing import List

def upper_first_letter(text: str):
    if text == "" or text is None:
        return text
    if len(text) == 1:
        return text.upper()
    return text[0].upper() + text[1:]

def underscore_to_camel(underscore: str) -> str:
    values = underscore.split("_")
    camel = values[0]
    if len(values) > 1:
        for value in values[1:]:
            camel += value.title()
    return camel

def wrap_by(text: str, start: str, end: str):
    return f"{start}{text}{end}"

def create_value_column(column: str):
    camel_column = underscore_to_camel(column)
    return wrap_by(camel_column, start="#{", end="}")


def create_update_column(column, check_empty: bool=False):
    update_column = '''
        <if test="@mybatis.Compare@notEmpty({0})">
            , {1} = {2}
        </if>
    '''.format(underscore_to_camel(column), column, f"#{{{underscore_to_camel(column)}}}")
    return update_column


def create_camel_columns(columns: List[str]):
    return [underscore_to_camel(column) for column in columns]
    

def create_update_column_list(columns: List[str]):
    return map(create_update_column, columns)


def create_map_to_object_code(object_name: str, camel_columns: List[str]):
    create_setter_code = lambda object_name, camel_column: f'{object_name}.set{upper_first_letter(camel_column)}(resultMap.getString("{camel_column}"))'
    setter_code = [create_setter_code(object_name, camel_column) for camel_column in camel_columns]
    spliter = ";\n"
    return f"{spliter.join(setter_code)}"


def  create_object_to_map_code(object_name: str, camel_columns: List[str]):
    first = "ParamMap.init()"
    create_put_code = lambda object_name, camel_column: f'put("{camel_column}", {object_name}.get{upper_first_letter(camel_column)}())'
    put_list = [create_put_code(object_name, camel_column) for camel_column in camel_columns]
    spliter = ".\n"
    return f'{first}.{spliter.join(put_list)}'



def create_insert_xml_code(table_name, method, columns):
    header = f'<insert id="{method}" parameterType="vifas.cmmn.ParamMap" useGeneratedKeys="true" keyProperty="id">'
    body_columns = f'({", ".join(columns)})' # example: (id, value, name)
    body_values = f'({", ".join(map(create_value_column, columns))})'
    footer = "</insert>"
    xml_code = '''
                {0}
                    insert into {1} {2}
                    values 
                        {3}
                {4}
    '''.format(header, table_name, body_columns, body_values, footer)
    return xml_code


def create_update_xml_code(table, method, key, columns):
    header = f'<update id="{method}" parameterType="vifas.cmmn.ParamMap">'
    update_column_list = create_update_column_list(columns=columns)
    update_body = "\n".join(update_column_list)
    footer = f'<update>'
    xml_code = '''
        {0}
            update {1} 
            set 
                {2}
            where
                {3} = {4}
        {5}
    '''.format(header, table, update_body, key, create_value_column(key), footer)
    return xml_code



if __name__ == "__main__":
    input_columns = [
       "foodentrps_seq",
        "entrps_nm",
        "rprsntv_nm",
        "entrps_adres",
        "la_crdnt_info",
        "lo_crdnt_info",
        "crtfctissu_at",
        "injryentrpsappn_at",
        "fsnreport_at",
        "crtfctissu_dt",
        "injryentrpsapn_at",
        "fsnreport_dt",
        "prduct_info",
        "creat_dt",
        "crtq_seq"
    ]

    with open("data.xml", "w") as f:
        insert_xml_code = create_insert_xml_code(table_name="foodentrps_info", method="register", columns=input_columns)
        update_xml_code = create_update_xml_code(table="foodentrps_info", method="update", key="foodentrps_seq", columns=input_columns)
        set_code = create_map_to_object_code("foodEntrpsVo", list(map(underscore_to_camel, input_columns)))
        put_code = create_object_to_map_code("foodEntrpsVo", list(map(underscore_to_camel, input_columns)))
        f.write(insert_xml_code)
        f.write("\n\n")
        f.write(update_xml_code)
        f.write("\n\n")
        f.write(set_code)
        f.write("\n\n")
        f.write(put_code)
    
