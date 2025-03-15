import bpy
import pymupdf
import bmesh
#a

rounds = 0

layers = {}


def createLines(layers):
    for key in layers:
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.active_object.name = key
        objectMesh = bpy.context.active_object.data
        bFA=bmesh.new()
        counter = 0
        evenCheck = 0

        #print(key)
        lines = layers.get(key)

        for vectors in lines:
            for vector in vectors:
                #print(vector)
                if vector == 0:
                    continue
                bFA.verts.new(vector)

        bFA.verts.ensure_lookup_table()

        for vectors in lines:    
            for vector in vectors:
                if vector == 0:
                    #counter = counter + 1
                    evenCheck = 0
                    #break
                    continue
                if evenCheck % 2 == 1:
                    bFA.edges.new([bFA.verts[counter-1],bFA.verts[counter]])
                counter = counter + 1
                evenCheck = evenCheck + 1
                #print(counter)

        bFA.verts.ensure_lookup_table()
        
        bFA.to_mesh(objectMesh)
        bFA.free()   


def extractLinesFromPdf(soubor):
    doc = pymupdf.open(soubor)
    
    for page in doc:
        #text = page.get_text()
        print('NOVA STRANKA')
        #image_list = page.get_images()
        #print(image_list)
        paths = page.get_drawings()
        #print(paths[0].keys())
        for path in paths:
            #print(path.get('layer'))
            layers[path.get('layer')] = list()
        #print(len(paths))
        counter = 0
        for path in paths:
            lines = []
            #print(path)
            #print()
            #if counter == 100000:
                #break
            listItems = path.get('items')
            typeD = path.get('type')
            if typeD == 'fs':
                continue
            for item in listItems:
                for prvek in item:
                    if type(prvek) == pymupdf.Point:
                        vector = (prvek[0],-prvek[1],0.0)
                        lines.append(vector)
            lines.append(0) 
            layers[path.get('layer')].append(lines)   
            #print(points)
            
            counter = counter + 1
            #print(counter)
            #return

        #print(len(points))
        #print(points)
        #return

        createLines(layers)


'''
    for page_num, page in enumerate(doc):
        shapes = page.get_drawings()  # Získání vektorových objektů
        for shape in shapes:
            for item in shape["items"]:
                if item[0] == "l":  # "l" znamená úsečka (line)
                    points = item[1]  # Souřadnice čáry

                    # Ověříme, že máme správný počet bodů
                    if len(points) == 4:
                        x0, y0, x1, y1 = points  # Správná extrakce bodů
                        lines.append(((x0, y0), (x1, y1)))
                    else:
                        print(f"Varování: Neočekávaný formát čáry na stránce {page_num + 1}: {points}")

    return lines
'''
# Použití
soubor = "vykres.pdf"
lines = extractLinesFromPdf(soubor)

