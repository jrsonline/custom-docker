import pkg_resources
imports={}
for i in In:
    if i.find("import") is 0 and i.find("pkg_resources") is -1 :
        library = i.split()[1]
        imports[library] = pkg_resources.get_distribution(library).version

print("# Add the below line/s to your requirements.txt file")
for imp in imports:
    print("{}=={}".format(imp,imports[imp]))
