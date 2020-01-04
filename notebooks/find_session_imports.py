import pkg_resources
import re

def _splitnl(str):
    return str.split('\n')

def _set_version_of(library, imports):
    try:
        imports[library] = pkg_resources.get_distribution(library).version
    except pkg_resources.DistributionNotFound:
        pass

def _get_deps_for(library, imports):
    try:
        deps = pkg_resources.working_set.by_key[library]
        for r in deps.requires():
            _set_version_of(r.project_name, imports)
            _get_deps_for(r.project_name, imports)
    except KeyError:
        pass
    
imports={}
for i in In:
    if i.find("import") is 0:
        library = re.split(r'\W+',i)[1]
        print(f"...have found an import of '{library}' in jupyter notebook history (from line '{_splitnl(i)[0]}')")
        _set_version_of(library, imports)
        _get_deps_for(library, imports)

print("# Add the below line/s to your requirements.txt file")
for imp in imports:
    print("{}=={}".format(imp,imports[imp]))
    
