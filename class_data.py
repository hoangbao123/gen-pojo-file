class ClassData:
    IDENT = "    "
    def __init__(self, class_name):
        self.class_name = class_name
        self.class_attributes = []
        self.inner_class = {}
    
    def gen_class_file(self, file_type='java'):
        if self.class_name is None or self.class_attributes is None:
            raise ValueError("Not enough data to gen class")
        else:
            if (file_type == 'java'):
                f = open(f"gen2/{self.class_name.capitalize()}.java", "w")
                self.gen_java_class(f)
            else:
                raise ValueError(f"File type {file_type} is not supported")
    
    def gen_java_class(self, fw, inner=False, num_indent=1):
        if not inner:
            fw.write(f"public class {self.class_name}" + "{ \n")
        else:
            fw.write(self.IDENT * (num_indent - 1) + f"public static class {self.class_name}" + "{ \n")

        for class_attribute in self.class_attributes:
            attr_name = class_attribute['name']
            attr_type = class_attribute['data_type']
            attr_gson = class_attribute['gson']
            attr_jackson = class_attribute['jackson']
            attr_column = class_attribute['column']
            # attr_name_type = class_attribute['name_type']
            if attr_gson is not None:
                fw.write(self.IDENT * num_indent + "@SerializedName(\"" + attr_gson + "\")"  + "\n")
            if attr_jackson is not None:
                fw.write(self.IDENT * num_indent + "@JsonProperty(\"" + attr_jackson + "\")" + "\n")
            if attr_column is not None:
                fw.write(self.IDENT * num_indent + "@Column(name = \"" + attr_column + "\")" + "\n")    
            fw.write(self.IDENT * num_indent + f"private {self.mapping_type(attr_type)} {attr_name};" + "\n")
            fw.write("\n")

        for k, v in self.inner_class.items():
            if v is not None:
                v.gen_java_class(fw, True, num_indent + 1)
            
        fw.write(self.IDENT * (num_indent - 1) + "} \n\n")


    def mapping_type(self, source_type: str, program_language='java'):
        des_type = None
        if source_type == 'tinyint' or source_type == 'smallint' or source_type == 'mediumint' or source_type == 'int':
            des_type = "Integer"
        elif source_type == 'bigint' or source_type == 'long':
            des_type = "Long"
        elif source_type == 'char' or source_type.lower().startswith("varchar") or source_type.lower() == "string":
            des_type = "String"
        elif source_type == 'json':
            des_type = "String"
        elif source_type.lower().startswith("bool"):
            des_type = "Boolean"
        elif source_type.lower() == "double" or source_type.lower() == "float":
            des_type = "Double"
        elif source_type.lower() == "timestamp":
            des_type = "ZonedDateTime"
        else:
            if source_type in self.inner_class:
                des_type = source_type 
            else:
                raise ValueError(f"This type '{source_type}' in {program_language} is not supported")

        return des_type