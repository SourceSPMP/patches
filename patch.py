import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python patch.py <dllpath> <patchname>")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        print("Provide a valid DLL path.")
        exit(1)
    patchfolder = "./patches/"+sys.argv[2]
    if not os.path.exists(patchfolder):
        print(f"Patch {sys.argv[2]} does not exist")
        exit(1)
    s = ""
    with open(sys.argv[1], "rb") as f:
        s = f.read()
    with open(os.path.join(patchfolder,"sig.txt"),"r") as f:
        signature = f.read()
    with open(os.path.join(patchfolder,"offset.txt"),"r") as f:
        offset = f.read()
    with open(os.path.join(patchfolder,"replacement.txt"),"r") as f:
        replacement = f.read()
    with open(os.path.join(patchfolder,"dllname.txt"),"r") as f:
        dllname = f.read()
    if dllname != os.path.basename(sys.argv[1]):
        print(f"The DLL name ({os.path.basename(sys.argv[1])}) does not match the one mentioned in the patch ({dllname}).\nDo you want to continue? (Y/N)")
        if(input().lower() != "y"):
            exit(1)
    hexes = signature.split(" ")
    bytesignature = bytes()
    for hex in hexes:
        bytesignature += bytes((int(hex,16),))
    bytereplacement = bytes()
    hexes = replacement.split(" ")
    for hex in hexes:
        bytereplacement += bytes((int(hex,16),))
    index = s.find(bytesignature)
    if index == -1:
        print("Could not find the patch signature in the specified DLL.")
        exit(1)
    index += int(offset)
    print(bytesignature)
    s = s[:index] + bytereplacement + s[index+len(bytereplacement):]
    patchedpath = os.path.basename(sys.argv[1]) + ".patched" + os.path.splitext(sys.argv[1])[1]
    if os.path.exists(patchedpath):
        os.remove(patchedpath)
    with open(patchedpath,"wb") as f:
        f.write(s)